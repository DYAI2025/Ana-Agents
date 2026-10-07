#!/usr/bin/env python3
"""Basic repository hygiene check (SPEC SEC-004, DATA-003, SYS-003).

This is a coarse guard for obvious mistakes, NOT a professional secret scanner. It checks
files in the git index (tracked or staged):

- HYG_TRACKED_ENV           .env / .env.* files (except .env.example)
- HYG_PRIVATE_PATH          private-data / runtime-data / export paths
- HYG_ROOT_RESEARCH_FILE    root-level .rtf/.doc/.docx/.pdf research or prompt files
- HYG_SECRET_PATTERN        a few well-known credential shapes
- HYG_UNSAFE_EMAIL          e-mail addresses outside reserved example domains
- HYG_FORBIDDEN_IMPORT      provider/framework SDK imports in the domain package

Exit status: 0 clean, 1 findings, 2 usage/environment error.
"""

from __future__ import annotations

import ast
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOMAIN_PACKAGE = Path("src/ana_agents")

PRIVATE_DIRS = frozenset({"private-research", "private-data", "runtime-data"})
PRIVATE_PREFIXES = ("crm-export", "contact-export", "suppression-export", "mail-export")
ROOT_RESEARCH_SUFFIXES = frozenset({".rtf", ".doc", ".docx", ".pdf"})

# Credential shapes. Assembled from parts so this file does not match itself.
SECRET_PATTERNS: dict[str, re.Pattern[str]] = {
    "aws-access-key-id": re.compile("AKIA" + r"[0-9A-Z]{16}"),
    "private-key-block": re.compile(
        "-----BEGIN " + r"(?:RSA |EC |OPENSSH |DSA )?" + "PRIVATE KEY-----"
    ),
    "github-token": re.compile("gh" + r"[pousr]_[A-Za-z0-9]{36,}"),
    "anthropic-key": re.compile("sk-" + r"ant-[A-Za-z0-9_-]{20,}"),
    "openai-style-key": re.compile("sk-" + r"(?:proj-)?[A-Za-z0-9]{32,}"),
    "slack-token": re.compile("xox" + r"[baprs]-[A-Za-z0-9-]{10,}"),
    "google-api-key": re.compile("AI" + r"za[0-9A-Za-z_-]{35}"),
    "zoho-oauth-token": re.compile("1000" + r"\.[0-9a-f]{32}\.[0-9a-f]{32}"),
}

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)\b")
# RFC 2606 / RFC 6761 reserved names. Real addresses never belong in this public repository.
SAFE_EMAIL_DOMAINS = ("example.invalid", "example.com", "example.org", "example.net")
SAFE_EMAIL_TLDS = (".invalid", ".test", ".example")

FORBIDDEN_IMPORT_ROOTS = frozenset(
    {
        "openai",
        "anthropic",
        "langchain",
        "langchain_core",
        "langgraph",
        "crewai",
        "autogen",
        "zoho",
        "zcrmsdk",
        "zohocrmsdk",
    }
)


@dataclass(frozen=True, order=True)
class HygieneFinding:
    code: str
    path: str
    detail: str


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True)
    return [p for p in result.stdout.decode("utf-8").split("\0") if p]


def _read_text(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\0" in data[:8192]:
        return None
    return data.decode("utf-8", errors="replace")


def email_is_safe(domain: str) -> bool:
    domain = domain.lower()
    if domain.endswith(SAFE_EMAIL_TLDS):
        return True
    return any(domain == d or domain.endswith("." + d) for d in SAFE_EMAIL_DOMAINS)


def check_path(path: str) -> list[HygieneFinding]:
    out: list[HygieneFinding] = []
    parts = Path(path).parts
    name = parts[-1]
    if (name == ".env" or name.startswith(".env.")) and name != ".env.example":
        out.append(HygieneFinding("HYG_TRACKED_ENV", path, "environment file is tracked"))
    if PRIVATE_DIRS.intersection(parts[:-1]) or name.startswith(PRIVATE_PREFIXES):
        out.append(HygieneFinding("HYG_PRIVATE_PATH", path, "private/runtime/export data path"))
    if len(parts) == 1 and Path(name).suffix.lower() in ROOT_RESEARCH_SUFFIXES:
        out.append(
            HygieneFinding("HYG_ROOT_RESEARCH_FILE", path, "root-level research/prompt document")
        )
    return out


def check_content(path: str, text: str) -> list[HygieneFinding]:
    out: list[HygieneFinding] = []
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            out.append(HygieneFinding("HYG_SECRET_PATTERN", path, f"looks like {label}"))
    for match in EMAIL_PATTERN.finditer(text):
        if not email_is_safe(match.group(1)):
            out.append(
                HygieneFinding(
                    "HYG_UNSAFE_EMAIL", path, f"address outside example domains: {match.group(0)}"
                )
            )
    return out


def forbidden_imports(source: str, path: str = "<string>") -> list[HygieneFinding]:
    """Provider/framework SDK imports (SYS-003). Parses imports; ignores strings/comments."""
    out: list[HygieneFinding] = []
    for node in ast.walk(ast.parse(source, filename=path)):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names = [node.module]
        for name in names:
            if name.split(".")[0] in FORBIDDEN_IMPORT_ROOTS:
                out.append(HygieneFinding("HYG_FORBIDDEN_IMPORT", path, f"imports {name}"))
    return out


def scan(root: Path) -> list[HygieneFinding]:
    findings: list[HygieneFinding] = []
    for rel in tracked_files(root):
        findings += check_path(rel)
        text = _read_text(root / rel)
        if text is None:
            continue
        findings += check_content(rel, text)
        if rel.endswith(".py") and Path(rel).is_relative_to(DOMAIN_PACKAGE):
            findings += forbidden_imports(text, rel)
    return sorted(set(findings))


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else REPO_ROOT
    try:
        findings = scan(root)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"check_repo_hygiene: cannot list tracked files in {root}: {exc}", file=sys.stderr)
        return 2
    for finding in findings:
        print(f"{finding.code}\t{finding.path}\t{finding.detail}")
    print(f"check_repo_hygiene: {len(tracked_files(root))} tracked files, {len(findings)} findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

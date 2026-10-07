#!/usr/bin/env python3
"""Deterministic structure, boundary and hygiene check of the ana-brand-intel package.

Standard library only, so it runs inside an installed package as well as in the repository.
It checks the package as shipped; it does not evaluate model behavior.

Findings (code  path  detail):
  PKG_MISSING          required file or directory missing or empty
  PKG_FRONTMATTER      SKILL.md frontmatter invalid (name/description)
  PKG_AGENT_META       agents/openai.yaml lacks a required key
  PKG_DANGLING_REF     SKILL.md or a reference names a package file that does not exist
  PKG_PIN              contracts/PINS.json entry missing or its sha256 does not match the file
  PKG_SCHEMA_REF       a pinned schema is not JSON or has a $ref to a missing schema file
  PKG_CAPABILITY       the allowed-capability list contains a forbidden capability, or the
                       forbidden list lacks one
  PKG_SECRET           a credential-shaped string
  PKG_UNSAFE_EMAIL     an e-mail address outside reserved example domains
  PKG_PRIVATE_DATA     a fixture declares production-protected data

Exit status: 0 clean, 1 findings, 2 usage error.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REQUIRED_FILES = ("SKILL.md", "agents/openai.yaml", "contracts/PINS.json", "evals/cases.yaml")
REQUIRED_DIRS = ("references", "contracts", "schemas", "evals", "scripts", "reports")
ALLOWED_CAPABILITIES = {"SEARCH", "WEB_READ", "CRM_READ", "KNOWLEDGE_READ"}
FORBIDDEN_CAPABILITIES = ("CRM_WRITE", "MAIL_SEND", "SEND authorization", "lifecycle mutation")
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".txt"}
SECRET_PATTERNS = {
    "aws-access-key-id": re.compile("AKIA" + r"[0-9A-Z]{16}"),
    "private-key-block": re.compile("-----BEGIN " + r"(?:RSA |EC |OPENSSH |DSA )?" + "PRIVATE KEY"),
    "github-token": re.compile("gh" + r"[pousr]_[A-Za-z0-9]{36,}"),
    "anthropic-key": re.compile("sk-" + r"ant-[A-Za-z0-9_-]{20,}"),
    "openai-style-key": re.compile("sk-" + r"(?:proj-)?[A-Za-z0-9]{32,}"),
    "google-api-key": re.compile("AI" + r"za[0-9A-Za-z_-]{35}"),
    "zoho-oauth-token": re.compile("1000" + r"\.[0-9a-f]{32}\.[0-9a-f]{32}"),
}
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)\b")
SAFE_EMAIL_SUFFIXES = (
    "example.invalid",
    "example.com",
    "example.org",
    "example.net",
    ".invalid",
    ".test",
    ".example",
)
FILE_REF = re.compile(r"`((?:references|contracts|schemas|evals|scripts|agents)/[A-Za-z0-9_./-]+)`")


def _frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        key, sep, value = line.partition(":")
        if not sep or not key.strip():
            return None
        fields[key.strip()] = value.strip()
    return fields


def _section(text: str, start: str, stop: str) -> str:
    i = text.find(start)
    j = text.find(stop, i + len(start)) if i >= 0 else -1
    return text[i:j] if i >= 0 and j >= 0 else ""


def check(skill_dir: Path) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for rel in REQUIRED_FILES:
        if not (skill_dir / rel).is_file():
            out.append(("PKG_MISSING", rel, "required file"))
    for rel in REQUIRED_DIRS:
        d = skill_dir / rel
        if not d.is_dir() or not any(p.is_file() for p in d.rglob("*")):
            out.append(("PKG_MISSING", rel + "/", "required non-empty directory"))
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return out
    text = skill_md.read_text(encoding="utf-8")

    fm = _frontmatter(text)
    if fm is None or set(fm) != {"name", "description"}:
        out.append(
            ("PKG_FRONTMATTER", "SKILL.md", "frontmatter must hold exactly name, description")
        )
    else:
        if fm["name"] != skill_dir.name:
            out.append(
                ("PKG_FRONTMATTER", "SKILL.md", f"name {fm['name']!r} != {skill_dir.name!r}")
            )
        if not 1 <= len(fm["description"]) <= 1024:
            out.append(("PKG_FRONTMATTER", "SKILL.md", "description must be 1..1024 chars"))

    meta = skill_dir / "agents" / "openai.yaml"
    if meta.is_file():
        meta_text = meta.read_text(encoding="utf-8")
        for key in ("interface:", "display_name:", "short_description:", "policy:"):
            if key not in meta_text:
                out.append(("PKG_AGENT_META", "agents/openai.yaml", f"missing {key}"))

    for doc in [skill_md, *sorted((skill_dir / "references").glob("*.md"))]:
        for ref in sorted(set(FILE_REF.findall(doc.read_text(encoding="utf-8")))):
            target = ref.rstrip("/")
            if not (skill_dir / target).exists():
                out.append(("PKG_DANGLING_REF", doc.relative_to(skill_dir).as_posix(), ref))

    pins_path = skill_dir / "contracts" / "PINS.json"
    if pins_path.is_file():
        pins = json.loads(pins_path.read_text(encoding="utf-8"))
        for pin in pins.get("pins", []):
            target = skill_dir / pin["path"]
            if not target.is_file():
                out.append(("PKG_PIN", pin["path"], "pinned file missing"))
            elif hashlib.sha256(target.read_bytes()).hexdigest() != pin["sha256"]:
                out.append(("PKG_PIN", pin["path"], "sha256 does not match PINS.json"))

    schema_names = {p.name for p in (skill_dir / "schemas").glob("*.json")}
    for schema in sorted((skill_dir / "schemas").glob("*.json")):
        try:
            refs = re.findall(r'"\$ref"\s*:\s*"([^"#]*)', schema.read_text(encoding="utf-8"))
            json.loads(schema.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            out.append(("PKG_SCHEMA_REF", schema.name, f"invalid JSON: {exc}"))
            continue
        for ref in refs:
            if ref and ref not in schema_names:
                out.append(("PKG_SCHEMA_REF", schema.name, f"$ref to missing {ref}"))

    allowed = _section(text, "Semantic capabilities that may be used", "Never widen")
    allowed_items = set(re.findall(r"^- ([A-Za-z_ ]+?)\s*$", allowed, re.MULTILINE))
    for item in sorted(allowed_items - ALLOWED_CAPABILITIES - {"structured artifact generation"}):
        out.append(("PKG_CAPABILITY", "SKILL.md", f"capability {item!r} is not allowed"))
    if not allowed_items:
        out.append(("PKG_CAPABILITY", "SKILL.md", "allowed-capability list not found"))
    forbidden = _section(text, "Forbidden:", "If a required read/search capability")
    for item in FORBIDDEN_CAPABILITIES:
        if f"- {item}" not in forbidden:
            out.append(("PKG_CAPABILITY", "SKILL.md", f"forbidden list lacks {item!r}"))

    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES or "__pycache__" in path.parts:
            continue
        rel = path.relative_to(skill_dir).as_posix()
        body = path.read_text(encoding="utf-8", errors="replace")
        if rel == "scripts/check_package.py":
            continue
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(body):
                out.append(("PKG_SECRET", rel, name))
        for match in EMAIL.finditer(body):
            if not match.group(1).lower().endswith(SAFE_EMAIL_SUFFIXES):
                out.append(("PKG_UNSAFE_EMAIL", rel, match.group(0)))
        if rel.startswith("evals/") and "PRODUCTION_PROTECTED" in body:
            out.append(("PKG_PRIVATE_DATA", rel, "fixture declares PRODUCTION_PROTECTED"))
    return sorted(set(out))


def main(argv: list[str]) -> int:
    if len(argv) > 2:
        print("usage: check_package.py [SKILL_DIR]")
        return 2
    skill_dir = Path(argv[1]).resolve() if len(argv) == 2 else SKILL_DIR
    findings = check(skill_dir)
    for code, path, detail in findings:
        print(f"{code}  {path}  {detail}")
    print(f"check_package: {skill_dir.name}, {len(findings)} findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

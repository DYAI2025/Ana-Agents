"""Repository hygiene gate (SEC-004, DATA-003): each detector must fire on a planted case."""

from __future__ import annotations

import subprocess
import sys

import pytest

from ana_agents import REPO_ROOT


def git_repo(tmp_path, files: dict[str, str | bytes]):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    for rel, content in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content)
    subprocess.run(["git", "add", "--", *files], cwd=tmp_path, check=True)
    return tmp_path


def run_script(root):
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "check_repo_hygiene.py"), str(root)],
        capture_output=True,
        text=True,
    )


def test_clean_synthetic_repo_passes(tmp_path):
    root = git_repo(
        tmp_path,
        {
            "README.md": "Contact partnerships@brand.example.com or ops@team.example.invalid.\n",
            ".env.example": "API_KEY=MISSING\n",
        },
    )
    result = run_script(root)
    assert result.returncode == 0, result.stdout


# Secret-like values are assembled at runtime so this test file never contains one.
PLANTED = {
    "aws": "AKIA" + "Q" * 16,
    "github": "ghp_" + "a1" * 18,
    "anthropic": "sk-" + "ant-" + "x" * 30,
    "slack": "xoxb-" + "1234567890-abcdef",
    "private-key": "-----BEGIN " + "RSA PRIVATE KEY-----",
    "zoho": "1000." + "a" * 32 + "." + "b" * 32,
}


@pytest.mark.parametrize("label", sorted(PLANTED))
def test_secret_pattern_is_detected(tmp_path, hygiene, label):
    root = git_repo(
        tmp_path, {"contracts/examples/leak.json": f'{{"token": "{PLANTED[label]}"}}\n'}
    )
    found = hygiene.scan(root)
    assert [f.code for f in found] == ["HYG_SECRET_PATTERN"]
    assert run_script(root).returncode == 1


@pytest.mark.parametrize(
    ("path", "code"),
    [
        (".env", "HYG_TRACKED_ENV"),
        ("config/.env.production", "HYG_TRACKED_ENV"),
        ("private-data/contacts.csv", "HYG_PRIVATE_PATH"),
        ("runtime-data/state.json", "HYG_PRIVATE_PATH"),
        ("crm-export-2026.csv", "HYG_PRIVATE_PATH"),
        ("Implementation-prompt.rtf", "HYG_ROOT_RESEARCH_FILE"),
        ("research.docx", "HYG_ROOT_RESEARCH_FILE"),
    ],
)
def test_unsafe_tracked_path_is_detected(tmp_path, hygiene, path, code):
    root = git_repo(tmp_path, {path: "x\n"})
    assert [f.code for f in hygiene.scan(root)] == [code]


def test_untracked_files_are_not_scanned(tmp_path, hygiene):
    root = git_repo(tmp_path, {"README.md": "ok\n"})
    (root / "Implementation-prompt.rtf").write_text("local only\n")
    assert hygiene.scan(root) == []


def test_real_looking_fixture_email_is_detected(tmp_path, hygiene):
    address = "jane.doe" + "@" + "gmail.com"
    root = git_repo(tmp_path, {"contracts/examples/valid/x.json": f'{{"email": "{address}"}}\n'})
    found = hygiene.scan(root)
    assert [f.code for f in found] == ["HYG_UNSAFE_EMAIL"]


@pytest.mark.parametrize(
    ("domain", "safe"),
    [
        ("example.com", True),
        ("brand.example.com", True),
        ("example.invalid", True),
        ("team.example.invalid", True),
        ("x.test", True),
        ("example.com.evil.io", False),
        ("notexample.com", False),
        ("gmail.com", False),
    ],
)
def test_email_domain_allowlist(hygiene, domain, safe):
    assert hygiene.email_is_safe(domain) is safe


def test_this_repository_is_clean(hygiene):
    """The gate runs against the real index; it must be green only because nothing is planted."""
    found = hygiene.scan(REPO_ROOT)
    assert found == [], [f"{f.code} {f.path} {f.detail}" for f in found]

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _seed(repo: Path) -> None:
    for name in ("ana-brand-intel", "ana-outreach-compose"):
        skill = repo / "skills" / name
        (skill / "agents").mkdir(parents=True)
        (skill / "reports").mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: test\ndescription: test\n---\n", encoding="utf-8")
        (skill / "agents" / "openai.yaml").write_text("interface:\n  display_name: Test\n", encoding="utf-8")
        (skill / "reports" / "release-status.json").write_text(
            json.dumps({"skill": name, "status": "BLOCKED", "release_authorized": False}),
            encoding="utf-8",
        )


def _run(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def test_candidate_packaging_is_reproducible_and_release_fails_closed(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    _seed(root)

    source_root = Path(__file__).resolve().parents[2]
    package = source_root / "scripts" / "package_skills.py"
    verify = source_root / "scripts" / "verify_release.py"

    args = (
        "--repo-root",
        str(root),
        "--mode",
        "candidate",
        "--repo-sha",
        "TESTSHA",
        "--build-timestamp",
        "2026-10-07T17:50:00Z",
    )
    first = _run(package, *args)
    assert first.returncode == 0, first.stderr

    candidate = root / "dist" / "candidate"
    checked = _run(verify, str(candidate))
    assert checked.returncode == 0, checked.stderr
    first_bytes = {
        p.name: p.read_bytes()
        for p in sorted(candidate.glob("*.zip"))
    }

    for p in candidate.iterdir():
        p.unlink()
    second = _run(package, *args)
    assert second.returncode == 0, second.stderr
    second_bytes = {
        p.name: p.read_bytes()
        for p in sorted(candidate.glob("*.zip"))
    }
    assert first_bytes == second_bytes

    blocked = _run(
        package,
        "--repo-root",
        str(root),
        "--mode",
        "release",
        "--repo-sha",
        "TESTSHA",
        "--build-timestamp",
        "2026-10-07T17:50:00Z",
    )
    assert blocked.returncode != 0
    assert "release blocked" in (blocked.stdout + blocked.stderr)

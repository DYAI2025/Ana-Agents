#!/usr/bin/env python3
"""Pin canonical repository contracts into an installable skill package.

An installed skill cannot read this repository, so the files it must bind to are carried
inside the package as byte-identical copies of the canonical sources. They are pins, not a
second contract family: ``skills/<name>/contracts/PINS.json`` lists every pinned file with
its canonical source path and sha256, and ``--check`` fails when a pin drifts from its
canonical source, when an unlisted file sits in a pinned directory, or when PINS.json is
stale. Canonical truth stays in ``contracts/``; fix drift by re-running without --check.

Exit status: 0 in sync (or written), 1 drift found, 2 usage/environment error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# skill name -> {destination path inside the skill: canonical repository path}
PIN_SETS: dict[str, dict[str, str]] = {
    "ana-brand-intel": {
        **{
            f"schemas/{name}.schema.json": f"contracts/schemas/{name}.schema.json"
            for name in (
                "common",
                "artifact-envelope",
                "source-record",
                "evidence-claim",
                "lead-triage",
                "creator-truth-pack",
                "brand-research",
                "contact-profile",
                "ana-brand-fit",
                "collaboration-hypothesis",
            )
        },
        "contracts/artifact-input-graph.yaml": "contracts/artifact-input-graph.yaml",
        **{
            f"contracts/policies/{name}": f"contracts/policies/{name}"
            for name in (
                "contact-policy.yaml",
                "contact-policy.md",
                "evidence-policy.md",
                "freshness-policy.md",
                "source-policy.md",
                "untrusted-content-policy.md",
            )
        },
    },
}
PINNED_DIRS = ("schemas", "contracts")
MANIFEST = "contracts/PINS.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def expected_manifest(skill: str, root: Path) -> dict:
    pins = []
    for dest, src in sorted(PIN_SETS[skill].items()):
        pins.append(
            {"path": dest, "canonical": src, "sha256": sha256_bytes((root / src).read_bytes())}
        )
    return {
        "description": (
            "Byte-identical pins of canonical DYAI2025/Ana-Agents contracts. Not a competing "
            "contract family: canonical truth is the repository path in `canonical`."
        ),
        "skill": skill,
        "pins": pins,
    }


def manifest_text(manifest: dict) -> str:
    return json.dumps(manifest, indent=2, sort_keys=True) + "\n"


def check(skill: str, root: Path) -> list[str]:
    skill_dir = root / "skills" / skill
    problems: list[str] = []
    for dest, src in sorted(PIN_SETS[skill].items()):
        pinned = skill_dir / dest
        if not pinned.is_file():
            problems.append(f"missing pin {dest} (canonical {src})")
        elif pinned.read_bytes() != (root / src).read_bytes():
            problems.append(f"pin {dest} differs from canonical {src}")
    allowed = set(PIN_SETS[skill]) | {MANIFEST}
    for directory in PINNED_DIRS:
        for path in sorted((skill_dir / directory).rglob("*")):
            if path.is_file():
                rel = path.relative_to(skill_dir).as_posix()
                if rel not in allowed:
                    problems.append(f"unlisted file in pinned directory: {rel}")
    manifest_path = skill_dir / MANIFEST
    want = manifest_text(expected_manifest(skill, root))
    if not manifest_path.is_file() or manifest_path.read_text(encoding="utf-8") != want:
        problems.append(f"{MANIFEST} is missing or stale")
    return problems


def write(skill: str, root: Path) -> None:
    skill_dir = root / "skills" / skill
    for dest, src in PIN_SETS[skill].items():
        target = skill_dir / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((root / src).read_bytes())
    (skill_dir / MANIFEST).write_text(
        manifest_text(expected_manifest(skill, root)), encoding="utf-8"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--skill", required=True, choices=sorted(PIN_SETS))
    ap.add_argument("--check", action="store_true", help="verify only; never write")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = ap.parse_args()
    root = args.repo_root.resolve()
    if not args.check:
        write(args.skill, root)
    problems = check(args.skill, root)
    for problem in problems:
        print(f"PIN_DRIFT {problem}")
    print(f"pins: {len(PIN_SETS[args.skill])} files, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

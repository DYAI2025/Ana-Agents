#!/usr/bin/env python3
"""Deterministically package Ana skill directories.

Candidate mode is allowed while release gates are blocked.
Release mode fails closed unless every selected skill reports release_authorized=true
for exactly the content digest being packaged (see skill_digest.py).

Per skill the output directory receives two byte-identical archives:
``<skill>/skill.zip`` (the primary install artifact named by the build contract) and
``<skill>.zip`` (the distribution copy). Both are listed in SHA256SUMS.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_digest import (
    ALGORITHM,
    content_digest,
    iter_package_files,
    sha256_bytes,
)

SKILLS = ("ana-brand-intel", "ana-outreach-compose")
REQUIRED = ("SKILL.md", "agents/openai.yaml")


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_gate(skill_dir: Path) -> dict:
    p = skill_dir / "reports" / "release-status.json"
    if not p.exists():
        raise SystemExit(f"missing release gate: {p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    if data.get("skill") != skill_dir.name:
        raise SystemExit(f"release gate skill mismatch: {p}")
    return data


def write_zip(skill_dir: Path, out: Path) -> None:
    for req in REQUIRED:
        if not (skill_dir / req).is_file():
            raise SystemExit(f"{skill_dir.name}: missing required file {req}")
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for src, rel in iter_package_files(skill_dir):
            info = zipfile.ZipInfo(rel.replace(os.sep, "/"), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, src.read_bytes())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--mode", choices=("candidate", "release"), default="candidate")
    ap.add_argument("--repo-sha", required=True)
    ap.add_argument(
        "--build-timestamp", required=True, help="explicit RFC3339 timestamp; never inferred"
    )
    ap.add_argument(
        "--skill",
        action="append",
        choices=SKILLS,
        help="package only this skill (repeatable); default: all skills",
    )
    args = ap.parse_args()

    root = args.repo_root.resolve()
    selected = tuple(args.skill) if args.skill else SKILLS
    out_dir = root / "dist" / ("candidate" if args.mode == "candidate" else "")
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema_version": "1.1.0",
        "mode": args.mode,
        "repository_sha": args.repo_sha,
        "build_timestamp": args.build_timestamp,
        "content_digest_algorithm": ALGORITHM,
        "artifacts": [],
    }

    for name in selected:
        skill_dir = root / "skills" / name
        gate = read_gate(skill_dir)
        digest = content_digest(skill_dir)
        if args.mode == "release":
            if gate.get("release_authorized") is not True:
                raise SystemExit(f"{name}: release blocked by reports/release-status.json")
            if gate.get("content_digest") != digest:
                raise SystemExit(
                    f"{name}: release authorization is for {gate.get('content_digest')!r}, "
                    f"package content is {digest!r}"
                )
        primary = out_dir / name / "skill.zip"
        write_zip(skill_dir, primary)
        copy = out_dir / f"{name}.zip"
        copy.write_bytes(primary.read_bytes())
        for target in (primary, copy):
            manifest["artifacts"].append(
                {
                    "skill": name,
                    "file": str(target.relative_to(root)).replace(os.sep, "/"),
                    "sha256": sha256_file(target),
                    "content_digest": digest,
                    "release_authorized": bool(gate.get("release_authorized")),
                    "gate_status": gate.get("status"),
                }
            )

    manifest_path = out_dir / "release-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    sums = out_dir / "SHA256SUMS"
    sums.write_text(
        "".join(
            f"{a['sha256']}  {Path(a['file']).relative_to(out_dir.relative_to(root)).as_posix()}\n"
            for a in manifest["artifacts"]
        ),
        encoding="utf-8",
    )
    print(f"{args.mode.upper()}_PACKAGE_CREATED {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

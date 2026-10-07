#!/usr/bin/env python3
"""Deterministically package Ana skill directories.

Candidate mode is allowed while release gates are blocked.
Release mode fails closed unless every skill reports release_authorized=true.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import zipfile

SKILLS = ("ana-brand-intel", "ana-outreach-compose")
REQUIRED = ("SKILL.md", "agents/openai.yaml")
EXCLUDE_NAMES = {".DS_Store"}
EXCLUDE_PARTS = {"__pycache__", ".pytest_cache", ".git", "dist"}

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_gate(skill_dir: Path) -> dict:
    p = skill_dir / "reports" / "release-status.json"
    if not p.exists():
        raise SystemExit(f"missing release gate: {p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    if data.get("skill") != skill_dir.name:
        raise SystemExit(f"release gate skill mismatch: {p}")
    return data

def iter_skill_files(skill_dir: Path):
    for p in sorted(skill_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(skill_dir)
        if p.name in EXCLUDE_NAMES or any(part in EXCLUDE_PARTS for part in rel.parts):
            continue
        yield p, rel

def write_zip(skill_dir: Path, out: Path) -> None:
    for req in REQUIRED:
        if not (skill_dir / req).is_file():
            raise SystemExit(f"{skill_dir.name}: missing required file {req}")
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for src, rel in iter_skill_files(skill_dir):
            info = zipfile.ZipInfo(str(rel).replace(os.sep, "/"), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, src.read_bytes())

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--mode", choices=("candidate", "release"), default="candidate")
    ap.add_argument("--repo-sha", required=True)
    ap.add_argument("--build-timestamp", required=True, help="explicit RFC3339 timestamp; never inferred")
    args = ap.parse_args()

    root = args.repo_root.resolve()
    out_dir = root / "dist" / ("candidate" if args.mode == "candidate" else "")
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema_version": "1.0.0",
        "mode": args.mode,
        "repository_sha": args.repo_sha,
        "build_timestamp": args.build_timestamp,
        "artifacts": [],
    }

    for name in SKILLS:
        skill_dir = root / "skills" / name
        gate = read_gate(skill_dir)
        if args.mode == "release" and gate.get("release_authorized") is not True:
            raise SystemExit(f"{name}: release blocked by reports/release-status.json")
        target = out_dir / f"{name}.zip"
        write_zip(skill_dir, target)
        manifest["artifacts"].append({
            "skill": name,
            "file": str(target.relative_to(root)).replace(os.sep, "/"),
            "sha256": sha256_file(target),
            "release_authorized": bool(gate.get("release_authorized")),
            "gate_status": gate.get("status"),
        })

    manifest_path = out_dir / "release-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    sums = out_dir / "SHA256SUMS"
    sums.write_text(
        "".join(f"{a['sha256']}  {Path(a['file']).name}\n" for a in manifest["artifacts"]),
        encoding="utf-8",
    )
    print(f"{args.mode.upper()}_PACKAGE_CREATED {out_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Verify Ana skill candidate/release artifacts against manifest/checksums."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

REQUIRED_ZIP = {"SKILL.md", "agents/openai.yaml"}

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("artifact_dir", type=Path)
    ap.add_argument("--require-release", action="store_true")
    args = ap.parse_args()

    d = args.artifact_dir.resolve()
    manifest = json.loads((d / "release-manifest.json").read_text(encoding="utf-8"))
    mode = manifest.get("mode")
    if args.require_release and mode != "release":
        raise SystemExit("candidate artifact cannot satisfy --require-release")

    expected_sums = {}
    for line in (d / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, name = line.split(None, 1)
        expected_sums[name.strip()] = digest

    for a in manifest.get("artifacts", []):
        p = d / Path(a["file"]).name
        actual = sha256_file(p)
        if actual != a["sha256"] or expected_sums.get(p.name) != actual:
            raise SystemExit(f"checksum mismatch: {p.name}")
        if args.require_release and a.get("release_authorized") is not True:
            raise SystemExit(f"release authorization missing: {a['skill']}")
        with zipfile.ZipFile(p) as zf:
            names = set(zf.namelist())
            if not REQUIRED_ZIP.issubset(names):
                raise SystemExit(f"{p.name}: required skill files missing")
            if any(n.startswith("/") or ".." in Path(n).parts for n in names):
                raise SystemExit(f"{p.name}: unsafe archive path")
    print("VERIFIED_RELEASE" if args.require_release else "VERIFIED_CANDIDATE")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

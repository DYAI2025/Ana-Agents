#!/usr/bin/env python3
"""Verify Ana skill candidate/release artifacts against manifest/checksums.

Checks per archive: sha256 matches both the manifest and SHA256SUMS; required control-plane
files are present; no absolute or parent-relative paths; the content digest recomputed
from the archive bytes equals the manifest's content digest. With ``--expect-digest
SKILL=sha256:...`` the archive must also carry exactly that content digest (binds eval or
release evidence to the bytes being shipped).
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_digest import digest_entries, sha256_bytes

REQUIRED_ZIP = {"SKILL.md", "agents/openai.yaml"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("artifact_dir", type=Path)
    ap.add_argument("--require-release", action="store_true")
    ap.add_argument("--expect-digest", action="append", default=[], metavar="SKILL=DIGEST")
    args = ap.parse_args()

    expected_digest = dict(item.split("=", 1) for item in args.expect_digest)
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

    seen_skills = set()
    for a in manifest.get("artifacts", []):
        rel = PurePosixPath(a["file"]).relative_to(PurePosixPath(a["file"]).parts[0])
        if mode == "candidate":
            rel = rel.relative_to("candidate")
        p = d / rel
        actual = sha256_bytes(p.read_bytes())
        if actual != a["sha256"] or expected_sums.get(rel.as_posix()) != actual:
            raise SystemExit(f"checksum mismatch: {rel}")
        if args.require_release and a.get("release_authorized") is not True:
            raise SystemExit(f"release authorization missing: {a['skill']}")
        with zipfile.ZipFile(p) as zf:
            names = set(zf.namelist())
            if not REQUIRED_ZIP.issubset(names):
                raise SystemExit(f"{rel}: required skill files missing")
            if any(n.startswith("/") or ".." in PurePosixPath(n).parts for n in names):
                raise SystemExit(f"{rel}: unsafe archive path")
            recomputed = digest_entries((n, zf.read(n)) for n in names if not n.endswith("/"))
        if recomputed != a.get("content_digest"):
            raise SystemExit(
                f"{rel}: content digest {recomputed} != manifest {a.get('content_digest')}"
            )
        want = expected_digest.get(a["skill"])
        if want is not None and recomputed != want:
            raise SystemExit(f"{rel}: content digest {recomputed} != expected {want}")
        seen_skills.add(a["skill"])
        print(f"  ok {rel} sha256={actual} content={recomputed}")
    missing = set(expected_digest) - seen_skills
    if missing:
        raise SystemExit(f"expected skills not in manifest: {sorted(missing)}")
    print("VERIFIED_RELEASE" if args.require_release else "VERIFIED_CANDIDATE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

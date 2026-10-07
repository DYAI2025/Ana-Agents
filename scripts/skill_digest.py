"""Content digest of an installable skill package.

The digest covers every packaged file except ``reports/``. ``reports/`` holds evidence
*about* a digest (eval runs, release status, build evidence), so it cannot be part of it
without a cycle. Eval evidence, release status and the archive manifest all name this
digest; ``verify_release.py`` recomputes it from the archive bytes.

Definition (``skill-content-v1``): sha256 over the UTF-8 lines
``<sha256 of file bytes>  <posix path relative to the skill root>\\n`` sorted by path.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Iterator
from pathlib import Path

ALGORITHM = "skill-content-v1"
EXCLUDE_NAMES = frozenset({".DS_Store"})
EXCLUDE_PARTS = frozenset({"__pycache__", ".pytest_cache", ".git", "dist"})
EVIDENCE_DIR = "reports"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def packaged(rel: str) -> bool:
    parts = rel.split("/")
    return parts[-1] not in EXCLUDE_NAMES and not EXCLUDE_PARTS.intersection(parts)


def iter_package_files(skill_dir: Path) -> Iterator[tuple[Path, str]]:
    for path in sorted(skill_dir.rglob("*")):
        if path.is_file():
            rel = path.relative_to(skill_dir).as_posix()
            if packaged(rel):
                yield path, rel


def digest_entries(entries: Iterable[tuple[str, bytes]]) -> str:
    lines = sorted(
        (rel, sha256_bytes(data))
        for rel, data in entries
        if packaged(rel) and rel.split("/")[0] != EVIDENCE_DIR
    )
    body = "".join(f"{file_hash}  {rel}\n" for rel, file_hash in lines)
    return "sha256:" + sha256_bytes(body.encode("utf-8"))


def content_digest(skill_dir: Path) -> str:
    return digest_entries((rel, path.read_bytes()) for path, rel in iter_package_files(skill_dir))

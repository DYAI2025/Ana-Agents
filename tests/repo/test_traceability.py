"""docs/TRACEABILITY.md covers every SPEC requirement with allowed states and real references."""

from __future__ import annotations

import re

from ana_agents import REPO_ROOT
from ana_agents.contracts.examples import load_negative_cases

SPEC = (REPO_ROOT / "SPEC.md").read_text(encoding="utf-8")
TRACE = (REPO_ROOT / "docs" / "TRACEABILITY.md").read_text(encoding="utf-8")
STATES = {"DEFINED", "IMPLEMENTED", "VERIFIED", "BLOCKED", "MISSING"}
ROW = re.compile(r"^\| ((?:SYS|INTEL|COMP|OPS|SEC|DATA|EVAL)-\d{3}) \|(.*)\| (\w+) \|$", re.M)


def rows():
    return [(m.group(1), m.group(2), m.group(3)) for m in ROW.finditer(TRACE)]


def test_every_spec_requirement_is_mapped():
    spec_ids = set(re.findall(r"^### ((?:SYS|INTEL|COMP|OPS|SEC|DATA|EVAL)-\d{3})", SPEC, re.M))
    assert len(spec_ids) == 41
    assert {r[0] for r in rows()} == spec_ids


def test_only_allowed_states():
    assert {r[2] for r in rows()} <= STATES


def test_verified_rows_reference_existing_tests_or_cases():
    case_ids = {c["id"] for c in load_negative_cases()}
    for req, body, state in rows():
        if state != "VERIFIED":
            continue
        test_files = re.findall(r"`((?:contracts|evidence|repo|skill_evals)/test_\w+\.py)`", body)
        cases = expand_case_refs(body)
        assert test_files or cases or "chain `" in body or "all `tests/`" in body, req
        for path in test_files:
            assert (REPO_ROOT / "tests" / path).is_file(), (req, path)
        for ref, matched in cases.items():
            assert matched <= case_ids and matched, (req, ref, sorted(matched - case_ids))


def expand_case_refs(body: str) -> dict[str, set[str]]:
    """`NEG-X-001`, `NEG-X-001..003` and `NEG-X-*` -> concrete case ids."""
    case_ids = {c["id"] for c in load_negative_cases()}
    refs: dict[str, set[str]] = {}
    for prefix, group, start, end in re.findall(
        r"`((?:NEG|POS))-([A-Z]+)-(\d{3}|\*)(?:\.\.(\d{3}))?`", body
    ):
        ref = f"{prefix}-{group}-{start}" + (f"..{end}" if end else "")
        if start == "*":
            refs[ref] = {c for c in case_ids if c.startswith(f"{prefix}-{group}-")}
        else:
            last = int(end) if end else int(start)
            refs[ref] = {f"{prefix}-{group}-{n:03d}" for n in range(int(start), last + 1)}
    return refs


def test_semantic_eval_rows_are_never_verified():
    for req, body, state in rows():
        if body.strip().startswith("eval |"):
            assert state in {"MISSING", "BLOCKED", "DEFINED"}, req

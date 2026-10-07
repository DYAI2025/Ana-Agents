"""Positive examples, valid chains and the negative-case manifest."""

from __future__ import annotations

import json

import pytest

from ana_agents.contracts.examples import (
    EXAMPLES_DIR,
    apply_ops,
    load_chain,
    load_negative_cases,
    run_case,
)
from ana_agents.contracts.registry import default_registry
from ana_agents.contracts.semantic import validate_artifact, validate_eval_case
from ana_agents.evidence.chain import validate_chain


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


VALID_EXAMPLES = sorted((EXAMPLES_DIR / "valid").glob("*.json"))
CHAINS = sorted((EXAMPLES_DIR / "chains").glob("*.json"))
CASES = load_negative_cases()

# Every negative proof the S1 brief requires, mapped to its manifest case(s).
REQUIRED_PROOFS = {
    "invalid epistemic status": ["NEG-EPI-001"],
    "FACT without evidence": ["NEG-EPI-002"],
    "FACT pointing to nonexistent source": ["NEG-EPI-003"],
    "UNKNOWN externally asserted": ["NEG-EPI-004", "NEG-EPI-005"],
    "HYPOTHESIS framed as FACT": ["NEG-EPI-006"],
    "SUPPORTED_INFERENCE without support": ["NEG-EPI-008", "NEG-EPI-009"],
    "used claim with unresolved material conflict": ["NEG-EPI-011"],
    "nonexistent claim reference": ["NEG-EPI-012"],
    "numeric/global fit score": ["NEG-FIT-001", "NEG-FIT-002"],
    "missing fit counterargument": ["NEG-FIT-004"],
    "ContactProfile used as AnaBrandFit dependency": ["NEG-FIT-005"],
    "private contact overstated as eligible": ["NEG-CON-001"],
    "unknown contact overstated as review/eligible": ["NEG-CON-002", "NEG-CON-003"],
    "public_found promoted to eligible": ["NEG-CON-004"],
    "missing Brand/Audience value": ["NEG-HYP-001", "NEG-HYP-002"],
    "EmailDraft dependent on raw BrandResearch/SourceRecord": ["NEG-GRAPH-001", "NEG-GRAPH-002"],
    "skill as SendPermission producer": ["NEG-SP-001"],
    "SendPermission with rejected approval": ["NEG-APP-001", "NEG-APP-002"],
    "approved draft whose outbound payload changed": ["NEG-DRAFT-001", "NEG-DRAFT-002"],
    "OPTED_OUT with send_authorized": ["NEG-SP-002"],
    "DNC with send_authorized": ["NEG-SP-003"],
    "hard bounce with send_authorized": ["NEG-SP-004"],
    "duplicate conflict with send_authorized": ["NEG-SP-006"],
    "unknown/not-configured compliance with send_authorized": ["NEG-SP-007", "NEG-SP-008"],
    "stale/not-evaluated freshness with send_authorized": ["NEG-SP-009", "NEG-SP-010"],
    "expired SendPermission": ["NEG-SP-011", "NEG-SP-012"],
    "stop_followups=false after reply": ["NEG-REP-001"],
    "classification before follow-up stop": ["NEG-REP-002"],
    "hard QA FAIL compensated by soft scores": ["NEG-QA-001"],
    "semantic eval PASS without execution": ["NEG-QA-002"],
    "dangling artifact reference": ["NEG-GRAPH-005"],
    "artifact dependency cycle": ["NEG-GRAPH-006"],
    "invalid timestamp": ["NEG-TIME-001", "NEG-TIME-002"],
    "draft after stop outcome": ["NEG-STOP-001", "NEG-STOP-002", "NEG-STOP-003"],
    "contact not ready": ["NEG-CON-006"],
    "QA not ready": ["NEG-QA-004"],
}


@pytest.mark.parametrize("path", VALID_EXAMPLES, ids=lambda p: p.name)
def test_positive_example_is_valid(path):
    doc = load_json(path)
    if "artifact_type" in doc:
        assert validate_artifact(doc) == []
    elif "eval_id" in doc:
        assert validate_eval_case(doc) == []
    elif "claim_id" in doc:
        assert default_registry().validate(doc, "EvidenceClaim") == []
    else:
        assert default_registry().validate(doc, "SourceRecord") == []


def test_every_pipeline_type_has_a_positive_example():
    types = {load_json(p).get("artifact_type") for p in VALID_EXAMPLES}
    assert default_registry().pipeline_types <= types


@pytest.mark.parametrize("path", CHAINS, ids=lambda p: p.stem)
def test_valid_chain_has_no_findings(path):
    chain = load_chain(path)
    assert validate_chain(chain.artifacts, now=chain.evaluated_at) == []


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_case_produces_exactly_the_expected_findings(case):
    result = run_case(case)
    assert result.actual == result.expected, [f.as_dict() for f in result.findings]


@pytest.mark.parametrize("case", [c for c in CASES if c["expect"]], ids=lambda c: c["id"])
def test_negative_case_base_is_valid_without_its_mutation(case):
    """Positive control: the unmutated base chain is clean, so the mutation is the cause."""
    chain = load_chain(EXAMPLES_DIR / case["base"])
    assert validate_chain(chain.artifacts, now=chain.evaluated_at) == []


def test_all_required_negative_proofs_are_present():
    ids = {c["id"] for c in CASES if c["expect"]}
    missing = {proof: refs for proof, refs in REQUIRED_PROOFS.items() if not set(refs) <= ids}
    assert missing == {}


def test_every_case_names_requirement_ids():
    for case in CASES:
        assert case["requirement_ids"], case["id"]


def test_case_runner_detects_a_wrong_expectation():
    """Canary: the exact-set comparison fails when the expectation is wrong."""
    case = dict(next(c for c in CASES if c["id"] == "NEG-SP-002"))
    case["expect"] = [{"code": "SEM_SEND_GATE_COMPLIANCE", "artifact": "sp-001"}]
    assert not run_case(case).passed
    case["expect"] = []
    assert not run_case(case).passed


def test_unknown_code_in_manifest_is_rejected():
    case = dict(CASES[0], expect=[{"code": "NOT_A_REAL_CODE", "artifact": "x"}])
    with pytest.raises(ValueError):
        run_case(case)


def test_apply_ops_does_not_mutate_the_base(send_chain):
    before = repr(send_chain.artifacts)
    apply_ops(
        send_chain,
        [{"op": "set", "artifact": "sp-001", "path": "/send_authorized", "value": False}],
    )
    assert repr(send_chain.artifacts) == before

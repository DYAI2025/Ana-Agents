"""Single-artifact semantic rules exercised directly (defense in depth behind the schema)."""

from __future__ import annotations

import json
from datetime import UTC, datetime

import pytest

from ana_agents.contracts import findings as F
from ana_agents.contracts.examples import EXAMPLES_DIR
from ana_agents.contracts.semantic import (
    check_semantics,
    grounded_claim_ids,
    validate_artifact,
    validate_eval_case,
)

EVAL_CASE = json.loads((EXAMPLES_DIR / "valid" / "eval-case.json").read_text())


def codes(found):
    return sorted(f.code for f in found)


@pytest.mark.parametrize("artifact_id", ["sp-001", "sr-001", "ha-001"])
def test_semantic_layer_rejects_skill_authority_even_if_schema_is_bypassed(artifacts, artifact_id):
    artifact = artifacts[artifact_id]
    artifact["producer"]["kind"] = "skill"
    assert F.SEM_SKILL_SEND_AUTHORITY in codes(check_semantics(artifact))


def test_skill_may_produce_drafts_and_research(artifacts):
    for artifact_id in ("br-001", "ed-001", "ch-001"):
        assert artifacts[artifact_id]["producer"]["kind"] == "skill"
        assert validate_artifact(artifacts[artifact_id]) == []


def test_schema_valid_send_permission_is_not_authorization_by_itself(artifacts):
    """A permission record can be schema-valid while denying sending; validity is not authority."""
    permission = artifacts["sp-001"]
    permission["send_authorized"] = False
    permission["block_reasons"] = ["compliance NOT_CONFIGURED"]
    assert validate_artifact(permission) == []


def test_expiry_is_checked_against_now(artifacts):
    permission = artifacts["sp-001"]
    before = datetime(2026, 10, 3, 9, 4, 59, tzinfo=UTC)
    at = datetime(2026, 10, 3, 9, 5, 0, tzinfo=UTC)
    assert validate_artifact(permission, now=before) == []
    assert codes(validate_artifact(permission, now=at)) == [F.SEM_SEND_PERMISSION_EXPIRED]


def test_all_gates_failing_reports_each_gate(artifacts):
    permission = artifacts["sp-001"]
    permission["gates"] = {
        "approval": "REJECTED",
        "qa": "NOT_READY",
        "contact_readiness": "REVIEW_REQUIRED",
        "compliance": "NOT_CONFIGURED",
        "suppression": "OPTED_OUT",
        "duplicate": "NOT_EVALUATED",
        "freshness": "STALE",
    }
    assert codes(check_semantics(permission)) == sorted(
        [
            F.SEM_SEND_GATE_APPROVAL,
            F.SEM_SEND_GATE_QA,
            F.SEM_SEND_GATE_CONTACT,
            F.SEM_SEND_GATE_COMPLIANCE,
            F.SEM_SEND_GATE_SUPPRESSION,
            F.SEM_SEND_GATE_DUPLICATE,
            F.SEM_SEND_GATE_FRESHNESS,
        ]
    )


def test_reply_semantic_layer_rejects_unstopped_followups(artifacts):
    reply = artifacts["rh-001"]
    reply["stop_followups"] = False
    assert codes(check_semantics(reply)) == [F.SEM_REPLY_FOLLOWUPS_NOT_STOPPED]


def test_reply_classification_at_stop_time_is_allowed(artifacts):
    reply = artifacts["rh-001"]
    reply["classification"]["classified_at"] = reply["followups_stopped_at"]
    assert validate_artifact(reply) == []


def test_eval_case_blocked_not_configured_is_valid():
    assert EVAL_CASE["result"]["status"] == "BLOCKED_NOT_CONFIGURED"
    assert validate_eval_case(EVAL_CASE) == []


@pytest.mark.parametrize(
    "result",
    [
        {"status": "PASS", "executed": False, "execution_ref": None, "executed_at": None},
        {
            "status": "PASS",
            "executed": True,
            "execution_ref": None,
            "executed_at": "2026-10-07T10:00:00Z",
        },
        {"status": "PASS", "executed": True, "execution_ref": "run-1", "executed_at": None},
        {"status": "FAIL", "executed": False, "execution_ref": None, "executed_at": None},
    ],
)
def test_eval_case_pass_or_fail_without_execution_evidence_is_rejected(result):
    case = dict(EVAL_CASE, result=result)
    assert codes(validate_eval_case(case)) == [F.SEM_EVAL_PASS_WITHOUT_EXECUTION]


def test_eval_case_pass_with_execution_evidence_is_accepted():
    case = dict(
        EVAL_CASE,
        result={
            "status": "PASS",
            "executed": True,
            "execution_ref": "run-eval-001",
            "executed_at": "2026-10-07T10:00:00Z",
        },
    )
    assert validate_eval_case(case) == []


def test_circular_inference_support_is_not_grounding():
    def claim(cid, status, sources=(), support=()):
        return {
            "claim_id": cid,
            "epistemic_status": status,
            "source_ids": list(sources),
            "supporting_claim_ids": list(support),
        }

    claims = [
        claim("a", "SUPPORTED_INFERENCE", support=["b"]),
        claim("b", "SUPPORTED_INFERENCE", support=["a"]),
        claim("c", "SUPPORTED_INFERENCE", support=["d"]),
        claim("d", "FACT", sources=["s"]),
    ]
    assert grounded_claim_ids(claims) == {"c", "d"}


def test_contact_outcome_ready_without_selected_contact_is_rejected(artifacts):
    profile = artifacts["cp-001"]
    profile["selected_contact_id"] = None
    assert codes(validate_artifact(profile)) == [F.SEM_CONTACT_OUTCOME_OVERSTATED]


def test_contact_policy_version_must_match(artifacts):
    profile = artifacts["cp-001"]
    profile["contact_policy_version"] = "0.9.0"
    assert codes(validate_artifact(profile)) == [F.SEM_CONTACT_POLICY_VERSION_MISMATCH]


def test_selected_contact_must_exist(artifacts):
    profile = artifacts["cp-001"]
    profile["selected_contact_id"] = "contact-404"
    assert codes(validate_artifact(profile)) == sorted(
        [F.SEM_UNRESOLVED_CONTACT, F.SEM_CONTACT_OUTCOME_OVERSTATED]
    )

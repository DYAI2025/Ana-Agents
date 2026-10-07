"""Cross-artifact chain rules that need direct construction rather than manifest mutations."""

from __future__ import annotations

import copy

from ana_agents.contracts import findings as F
from ana_agents.evidence.chain import InputGraph, load_input_graph, stop_reason, validate_chain


def project(found):
    return sorted({(f.code, f.artifact_id) for f in found})


def test_duplicate_artifact_id_is_reported_once_and_fails_closed(send_chain):
    artifacts = copy.deepcopy(send_chain.artifacts)
    duplicate = copy.deepcopy(next(a for a in artifacts if a["artifact_id"] == "or-001"))
    artifacts.append(duplicate)
    assert project(validate_chain(artifacts, now=send_chain.evaluated_at)) == [
        (F.CHAIN_DUPLICATE_ARTIFACT_ID, "or-001")
    ]


def test_cycle_detected_in_isolation_with_a_permissive_graph(send_chain):
    """Prove cycle detection independent of the input-type rule."""
    strict = load_input_graph()
    everything = frozenset(strict.allowed)
    permissive = InputGraph(
        strict.version,
        {name: everything for name in strict.allowed},
        {name: frozenset() for name in strict.allowed},
        {name: 0 for name in strict.allowed},
    )
    artifacts = copy.deepcopy(send_chain.artifacts)
    lead = next(a for a in artifacts if a["artifact_id"] == "lt-001")
    lead["input_artifact_ids"] = ["or-001"]
    found = validate_chain(artifacts, now=send_chain.evaluated_at, graph=permissive)
    assert {f.code for f in found} == {F.CHAIN_CYCLE}
    assert len(found) == 1


def test_self_reference_is_a_cycle(send_chain):
    artifacts = copy.deepcopy(send_chain.artifacts)
    outcome = next(a for a in artifacts if a["artifact_id"] == "or-001")
    outcome["input_artifact_ids"].append("or-001")
    codes = {f.code for f in validate_chain(artifacts, now=send_chain.evaluated_at)}
    assert F.CHAIN_CYCLE in codes


def test_cross_artifact_claim_id_collision(send_chain):
    artifacts = copy.deepcopy(send_chain.artifacts)
    pack = next(a for a in artifacts if a["artifact_id"] == "ctp-001")
    pack["claims"][0]["claim_id"] = "clm-br-1"
    pack["claims"][0]["epistemic_status"] = "HYPOTHESIS"
    pack["claims"][0]["source_ids"] = []
    codes = {f.code for f in validate_chain(artifacts, now=send_chain.evaluated_at)}
    assert F.CHAIN_DUPLICATE_CLAIM_ID in codes


def test_stop_reasons():
    assert stop_reason({"artifact_type": "AnaBrandFit", "fit_outcome": "WEAK_FIT"}) is None
    assert stop_reason({"artifact_type": "AnaBrandFit", "fit_outcome": "NO_FIT"}) == "NO_FIT"
    assert stop_reason({"artifact_type": "CommercialCheck", "status": "REVIEW"}) is None
    assert stop_reason({"artifact_type": "LeadTriage", "triage_outcome": "DEFER"}) == "triage DEFER"
    assert (
        stop_reason({"artifact_type": "ContactProfile", "contact_outcome": "CONTACT_NOT_READY"})
        == "CONTACT_NOT_READY"
    )


def test_outcome_record_may_follow_any_stop(send_chain):
    """NO_FIT et al. are successful outcomes: an OutcomeRecord after them is valid."""
    artifacts = [
        copy.deepcopy(a)
        for a in send_chain.artifacts
        if a["artifact_id"] in {"lt-001", "ctp-001", "br-001", "fit-001", "or-001"}
    ]
    fit = next(a for a in artifacts if a["artifact_id"] == "fit-001")
    fit["fit_outcome"] = "CONFLICTING_EVIDENCE"
    outcome = next(a for a in artifacts if a["artifact_id"] == "or-001")
    outcome["input_artifact_ids"] = ["fit-001"]
    outcome["outcome"] = "CONFLICTING_EVIDENCE"
    assert validate_chain(artifacts, now=send_chain.evaluated_at) == []


def test_schema_invalid_upstream_does_not_cascade(send_chain):
    artifacts = copy.deepcopy(send_chain.artifacts)
    research = next(a for a in artifacts if a["artifact_id"] == "br-001")
    research["claims"][0]["epistemic_status"] = "MAYBE"
    assert project(validate_chain(artifacts, now=send_chain.evaluated_at)) == [
        (F.SCHEMA_INVALID, "br-001")
    ]


def test_non_object_entries_are_reported(send_chain):
    artifacts = [*copy.deepcopy(send_chain.artifacts), "not-an-artifact"]
    assert project(validate_chain(artifacts, now=send_chain.evaluated_at)) == [
        (F.REGISTRY_NOT_AN_OBJECT, None)
    ]

"""Single-artifact semantic validation (ADR-003, JSON Schema vs Python boundary).

JSON Schema owns shape: types, enums, required fields, local conditional presence.
This module owns rules that need values, policy or time: id resolution inside one
artifact, contact-policy readiness, hard-check non-compensation, execution evidence,
SendPermission internal consistency and expiry, reply stop ordering, producer authority.

Semantic rules only run on schema-valid artifacts, so the code may rely on the shape.
A clean result means "consistent with the contract", never "true" and never "authorized".
"""

from __future__ import annotations

import functools
from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from ana_agents import CONTRACTS_DIR
from ana_agents.contracts import findings as F
from ana_agents.contracts.findings import Finding
from ana_agents.contracts.hashing import compute_draft_hash
from ana_agents.contracts.registry import SchemaRegistry, default_registry

CONTACT_POLICY_PATH = CONTRACTS_DIR / "policies" / "contact-policy.yaml"

# Artifacts that carry approval or send authority and the only producer kind allowed for each.
AUTHORITY_PRODUCERS = {
    "HumanApproval": "human",
    "SendPermission": "runtime",
    "SendReceipt": "runtime",
}

# Gate values that allow send_authorized=true. Anything else blocks (fail-closed).
SEND_GATE_REQUIREMENTS: dict[str, tuple[str, str]] = {
    "approval": ("APPROVED", F.SEM_SEND_GATE_APPROVAL),
    "qa": ("READY_FOR_HUMAN_REVIEW", F.SEM_SEND_GATE_QA),
    "contact_readiness": ("ELIGIBLE_FOR_GATES", F.SEM_SEND_GATE_CONTACT),
    "compliance": ("CLEARED", F.SEM_SEND_GATE_COMPLIANCE),
    "suppression": ("CLEAR", F.SEM_SEND_GATE_SUPPRESSION),
    "duplicate": ("CLEAR", F.SEM_SEND_GATE_DUPLICATE),
    "freshness": ("FRESH", F.SEM_SEND_GATE_FRESHNESS),
}

GROUNDING_STATUSES = frozenset({"FACT", "SUPPORTED_INFERENCE"})


def parse_timestamp(value: str) -> datetime:
    """Parse an RFC 3339 timestamp that already passed format checking."""
    parsed = datetime.fromisoformat(value.upper().replace("Z", "+00:00"))
    if parsed.tzinfo is None:  # pragma: no cover - format checker rejects naive values
        raise ValueError(f"timestamp without offset: {value!r}")
    return parsed


# -- contact policy ------------------------------------------------------------------------


class ContactPolicyError(Exception):
    pass


@dataclass(frozen=True)
class ContactRule:
    rule_id: str
    when: Mapping[str, Any]
    readiness: str


@dataclass(frozen=True)
class ContactPolicy:
    version: str
    order: tuple[str, ...]
    default: str
    rules: tuple[ContactRule, ...]

    def rank(self, readiness: str) -> int:
        return self.order.index(readiness)

    def most_restrictive(self, values: Iterable[str]) -> str:
        return max(values, key=self.rank)

    def evaluate(
        self, source_class: str, verification: str, public_business_context: bool
    ) -> tuple[str, tuple[str, ...]]:
        """Return (readiness, matched rule ids). Most restrictive match wins; none -> default."""
        facts = {
            "source_class": source_class,
            "verification": verification,
            "public_business_context": public_business_context,
        }
        matched = [
            rule
            for rule in self.rules
            if all(facts[key] == value for key, value in rule.when.items())
        ]
        if not matched:
            return self.default, ()
        return (
            self.most_restrictive(rule.readiness for rule in matched),
            tuple(rule.rule_id for rule in matched),
        )

    def effective_readiness(self, contact: Mapping[str, Any]) -> str:
        """Most restrictive of the declared and the policy-derived readiness."""
        computed, _ = self.evaluate(
            contact["source_class"], contact["verification"], contact["public_business_context"]
        )
        return self.most_restrictive((computed, contact["readiness"]))


def load_contact_policy(
    path: Path = CONTACT_POLICY_PATH, registry: SchemaRegistry | None = None
) -> ContactPolicy:
    registry = registry or default_registry()
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    problems = registry.validate(data, "ContactPolicy")
    if problems:
        raise ContactPolicyError("; ".join(f"{p.path} {p.message}" for p in problems))
    ids = [rule["id"] for rule in data["rules"]]
    if len(ids) != len(set(ids)):
        raise ContactPolicyError(f"duplicate rule ids in {path}")
    return ContactPolicy(
        version=data["policy_version"],
        order=tuple(data["readiness_order"]),
        default=data["default_readiness"],
        rules=tuple(ContactRule(r["id"], dict(r["when"]), r["readiness"]) for r in data["rules"]),
    )


@functools.cache
def default_contact_policy() -> ContactPolicy:
    return load_contact_policy()


# -- helpers -------------------------------------------------------------------------------


def _duplicates(values: Iterable[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def _dup_findings(artifact_id: str, path: str, values: Iterable[str]) -> list[Finding]:
    return [
        Finding(F.SEM_DUPLICATE_ID, artifact_id, path, f"duplicate id {value!r}")
        for value in _duplicates(values)
    ]


def grounded_claim_ids(claims: Iterable[Mapping[str, Any]]) -> set[str]:
    """Claims with real support: FACT/SUPPORTED_INFERENCE backed by sources, or (for
    SUPPORTED_INFERENCE) by another grounded claim. Circular inference support is not
    grounding. Resolution of source ids is checked separately."""
    claims = list(claims)
    grounded = {
        c["claim_id"]
        for c in claims
        if c["epistemic_status"] in GROUNDING_STATUSES and c["source_ids"]
    }
    changed = True
    while changed:
        changed = False
        for claim in claims:
            if claim["claim_id"] in grounded or claim["epistemic_status"] != "SUPPORTED_INFERENCE":
                continue
            support = set(claim["supporting_claim_ids"]) - {claim["claim_id"]}
            if support & grounded:
                grounded.add(claim["claim_id"])
                changed = True
    return grounded


def _execution_findings(
    artifact_id: str | None, path: str, result: Mapping[str, Any]
) -> list[Finding]:
    if result["status"] not in ("PASS", "FAIL"):
        return []
    if result["executed"] and result["execution_ref"] and result["executed_at"]:
        return []
    return [
        Finding(
            F.SEM_EVAL_PASS_WITHOUT_EXECUTION,
            artifact_id,
            path,
            f"result {result['status']} reported without execution evidence "
            "(executed, execution_ref, executed_at required); "
            "use NOT_RUN or BLOCKED_NOT_CONFIGURED",
        )
    ]


# -- per-type rules ------------------------------------------------------------------------


def _check_research(artifact: Mapping[str, Any]) -> list[Finding]:
    aid = artifact["artifact_id"]
    out: list[Finding] = []
    sources = artifact["sources"]
    claims = artifact["claims"]
    out += _dup_findings(aid, "/sources", (s["source_id"] for s in sources))
    out += _dup_findings(aid, "/claims", (c["claim_id"] for c in claims))
    source_ids = {s["source_id"] for s in sources}
    claim_ids = {c["claim_id"] for c in claims}
    for index, claim in enumerate(claims):
        base = f"/claims/{index}"
        for sid in claim["source_ids"]:
            if sid not in source_ids:
                out.append(
                    Finding(
                        F.SEM_UNRESOLVED_SOURCE,
                        aid,
                        f"{base}/source_ids",
                        f"unknown source {sid!r}",
                    )
                )
        for cid in claim["supporting_claim_ids"]:
            if cid not in claim_ids:
                out.append(
                    Finding(
                        F.SEM_UNRESOLVED_CLAIM,
                        aid,
                        f"{base}/supporting_claim_ids",
                        f"unknown claim {cid!r}",
                    )
                )
        for cid in claim["conflict"]["conflicting_claim_ids"]:
            if cid not in claim_ids:
                out.append(
                    Finding(
                        F.SEM_UNRESOLVED_CLAIM,
                        aid,
                        f"{base}/conflict/conflicting_claim_ids",
                        f"unknown conflicting claim {cid!r}",
                    )
                )
    grounded = grounded_claim_ids(claims)
    for index, claim in enumerate(claims):
        if claim["epistemic_status"] == "SUPPORTED_INFERENCE" and claim["claim_id"] not in grounded:
            out.append(
                Finding(
                    F.SEM_UNSUPPORTED_INFERENCE,
                    aid,
                    f"/claims/{index}",
                    "SUPPORTED_INFERENCE has no source and no grounded supporting claim",
                )
            )
    return out


def _check_contact_profile(artifact: Mapping[str, Any], policy: ContactPolicy) -> list[Finding]:
    aid = artifact["artifact_id"]
    out: list[Finding] = []
    if artifact["contact_policy_version"] != policy.version:
        out.append(
            Finding(
                F.SEM_CONTACT_POLICY_VERSION_MISMATCH,
                aid,
                "/contact_policy_version",
                f"profile uses {artifact['contact_policy_version']!r}, "
                f"policy is {policy.version!r}",
            )
        )
    contacts = artifact["contacts"]
    out += _dup_findings(aid, "/contacts", (c["contact_id"] for c in contacts))
    for index, contact in enumerate(contacts):
        computed, rules = policy.evaluate(
            contact["source_class"], contact["verification"], contact["public_business_context"]
        )
        if policy.rank(contact["readiness"]) < policy.rank(computed):
            out.append(
                Finding(
                    F.SEM_CONTACT_READINESS_OVERSTATED,
                    aid,
                    f"/contacts/{index}/readiness",
                    f"declared {contact['readiness']} but contact policy yields {computed} "
                    f"(rules {', '.join(rules) or 'default'})",
                )
            )
    selected_id = artifact["selected_contact_id"]
    by_id = {c["contact_id"]: c for c in contacts}
    if selected_id is not None and selected_id not in by_id:
        out.append(
            Finding(
                F.SEM_UNRESOLVED_CONTACT,
                aid,
                "/selected_contact_id",
                f"unknown contact {selected_id!r}",
            )
        )
    if artifact["contact_outcome"] == "READY_FOR_GATES":
        selected = by_id.get(selected_id) if selected_id is not None else None
        if selected is None or policy.effective_readiness(selected) != "ELIGIBLE_FOR_GATES":
            out.append(
                Finding(
                    F.SEM_CONTACT_OUTCOME_OVERSTATED,
                    aid,
                    "/contact_outcome",
                    "READY_FOR_GATES requires a selected contact whose effective readiness is "
                    "ELIGIBLE_FOR_GATES; otherwise the outcome is CONTACT_NOT_READY (INTEL-010)",
                )
            )
    return out


def _check_commercial(artifact: Mapping[str, Any]) -> list[Finding]:
    if artifact["status"] == "VIABLE" and artifact["commercial_policy"]["status"] == "MISSING":
        return [
            Finding(
                F.SEM_COMMERCIAL_VIABLE_WITHOUT_POLICY,
                artifact["artifact_id"],
                "/status",
                "VIABLE requires a configured commercial policy; real values are MISSING",
            )
        ]
    return []


def _check_email_draft(artifact: Mapping[str, Any]) -> list[Finding]:
    aid = artifact["artifact_id"]
    out = _dup_findings(aid, "/claim_usage", (u["claim_id"] for u in artifact["claim_usage"]))
    expected = compute_draft_hash(artifact)
    if artifact["draft_hash"] != expected:
        out.append(
            Finding(
                F.SEM_DRAFT_HASH_MISMATCH,
                aid,
                "/draft_hash",
                f"declared draft_hash does not match send_payload hash {expected}",
            )
        )
    return out


def _check_qa(artifact: Mapping[str, Any]) -> list[Finding]:
    aid = artifact["artifact_id"]
    checks = artifact["hard_checks"]
    out = _dup_findings(aid, "/hard_checks", (c["check_id"] for c in checks))
    for index, check in enumerate(checks):
        out += _execution_findings(aid, f"/hard_checks/{index}/result", check["result"])
    not_passed = [c["check_id"] for c in checks if c["result"]["status"] != "PASS"]
    if not_passed and artifact["overall"] != "NOT_READY":
        out.append(
            Finding(
                F.SEM_QA_HARD_FAIL_COMPENSATED,
                aid,
                "/overall",
                f"hard checks not passed ({', '.join(not_passed)}); soft scores cannot compensate",
            )
        )
    return out


def _check_send_permission(artifact: Mapping[str, Any], now: datetime | None) -> list[Finding]:
    aid = artifact["artifact_id"]
    out: list[Finding] = []
    issued = parse_timestamp(artifact["issued_at"])
    expires = parse_timestamp(artifact["expires_at"])
    authorized = artifact["send_authorized"]
    if expires <= issued:
        out.append(
            Finding(
                F.SEM_SEND_PERMISSION_INCONSISTENT,
                aid,
                "/expires_at",
                "expires_at must be after issued_at",
            )
        )
    if authorized and artifact["block_reasons"]:
        out.append(
            Finding(
                F.SEM_SEND_PERMISSION_INCONSISTENT,
                aid,
                "/block_reasons",
                "send_authorized=true with block reasons",
            )
        )
    if not authorized and not artifact["block_reasons"]:
        out.append(
            Finding(
                F.SEM_SEND_PERMISSION_INCONSISTENT,
                aid,
                "/block_reasons",
                "send_authorized=false requires at least one block reason",
            )
        )
    inputs = set(artifact["input_artifact_ids"])
    bindings = artifact["bindings"]
    for key in (
        "draft_artifact_id",
        "approval_artifact_id",
        "qa_report_artifact_id",
        "contact_profile_artifact_id",
    ):
        if bindings[key] not in inputs:
            out.append(
                Finding(
                    F.SEM_SEND_PERMISSION_INCONSISTENT,
                    aid,
                    f"/bindings/{key}",
                    f"binding {bindings[key]!r} is not among input_artifact_ids",
                )
            )
    if authorized:
        for gate, (required, code) in SEND_GATE_REQUIREMENTS.items():
            actual = artifact["gates"][gate]
            if actual != required:
                out.append(
                    Finding(
                        code,
                        aid,
                        f"/gates/{gate}",
                        f"send_authorized=true requires {gate}={required}, got {actual}",
                    )
                )
        if now is not None and now >= expires:
            out.append(
                Finding(
                    F.SEM_SEND_PERMISSION_EXPIRED,
                    aid,
                    "/expires_at",
                    f"permission expired at {artifact['expires_at']}",
                )
            )
    return out


def _check_reply(artifact: Mapping[str, Any]) -> list[Finding]:
    aid = artifact["artifact_id"]
    out: list[Finding] = []
    if artifact["stop_followups"] is not True:  # pragma: no cover - schema const guards this
        out.append(
            Finding(
                F.SEM_REPLY_FOLLOWUPS_NOT_STOPPED, aid, "/stop_followups", "follow-ups not stopped"
            )
        )
    classification = artifact.get("classification")
    if classification is not None:
        stopped = parse_timestamp(artifact["followups_stopped_at"])
        classified = parse_timestamp(classification["classified_at"])
        if classified < stopped:
            out.append(
                Finding(
                    F.SEM_REPLY_CLASSIFIED_BEFORE_STOP,
                    aid,
                    "/classification/classified_at",
                    "reply was classified before follow-ups were stopped (OPS-008)",
                )
            )
    return out


def _check_producer_authority(artifact: Mapping[str, Any]) -> list[Finding]:
    required = AUTHORITY_PRODUCERS.get(artifact["artifact_type"])
    actual = artifact["producer"]["kind"]
    if required is None or actual == required:
        return []
    return [
        Finding(
            F.SEM_SKILL_SEND_AUTHORITY,
            artifact["artifact_id"],
            "/producer/kind",
            f"{artifact['artifact_type']} must be produced by {required}, not {actual}; "
            "generative skills never create approval or send authority (OPS-001)",
        )
    ]


def check_semantics(
    artifact: Mapping[str, Any],
    *,
    now: datetime | None = None,
    policy: ContactPolicy | None = None,
) -> list[Finding]:
    """Semantic rules for one schema-valid pipeline artifact."""
    kind = artifact["artifact_type"]
    out = _check_producer_authority(artifact)
    if kind in ("BrandResearch", "CreatorTruthPack"):
        out += _check_research(artifact)
    elif kind == "ContactProfile":
        out += _check_contact_profile(artifact, policy or default_contact_policy())
    elif kind == "AnaBrandFit":
        out += _dup_findings(
            artifact["artifact_id"], "/dimensions", (d["dimension"] for d in artifact["dimensions"])
        )
    elif kind == "CollaborationHypothesis":
        out += _dup_findings(
            artifact["artifact_id"],
            "/hypotheses",
            (h["hypothesis_id"] for h in artifact["hypotheses"]),
        )
    elif kind == "CommercialCheck":
        out += _check_commercial(artifact)
    elif kind == "EmailDraft":
        out += _check_email_draft(artifact)
    elif kind == "QAGateReport":
        out += _check_qa(artifact)
    elif kind == "SendPermission":
        out += _check_send_permission(artifact, now)
    elif kind == "ReplyHandoff":
        out += _check_reply(artifact)
    return out


def validate_artifact(
    artifact: Any,
    *,
    now: datetime | None = None,
    registry: SchemaRegistry | None = None,
    policy: ContactPolicy | None = None,
) -> list[Finding]:
    """Schema validation, then semantic rules if the schema passed."""
    registry = registry or default_registry()
    schema_findings = registry.validate_artifact(artifact)
    if schema_findings:
        return schema_findings
    return check_semantics(artifact, now=now, policy=policy)


def validate_eval_case(case: Any, *, registry: SchemaRegistry | None = None) -> list[Finding]:
    registry = registry or default_registry()
    eval_id = case.get("eval_id") if isinstance(case, dict) else None
    schema_findings = registry.validate(case, "EvalCase", eval_id)
    if schema_findings:
        return schema_findings
    return _execution_findings(eval_id, "/result", case["result"])

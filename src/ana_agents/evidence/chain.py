"""Cross-artifact evidence-chain validation (ADR-003).

``validate_chain`` takes every artifact of one lead/run and returns all findings from
three layers: schema, single-artifact semantics and the chain rules below. An empty
result means the chain is internally consistent with the contract. It is not proof that
any claim is true and it is never send authorization.

Chain rules:

- artifact ids are unique; every input id resolves; the input graph is acyclic;
- every artifact carries the chain's single ``run_id``; LeadTriage, BrandResearch and
  ContactProfile name the same Brand id;
- input types follow contracts/artifact-input-graph.yaml (allowed, required, one per type);
- nothing but an OutcomeRecord may follow a stop outcome (NO_FIT, INSUFFICIENT_EVIDENCE,
  CONFLICTING_EVIDENCE, triage DEFER/REJECT, NOT_VIABLE, CONTACT_NOT_READY);
- claim and source references resolve within the artifact's ancestry;
- external framing respects the epistemic status of each used claim;
- used claims with an unresolved material conflict block;
- draft hash, approval, QA, contact and SendPermission bindings agree with the actual
  upstream artifacts; SendReceipt stays within an authorized, unexpired permission.

Content checks are skipped for schema-invalid artifacts (their schema finding already
fails the chain), so one structural defect does not cascade into unrelated noise.
"""

from __future__ import annotations

import functools
from collections import Counter
from collections.abc import Mapping, Sequence
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
from ana_agents.contracts.semantic import (
    ContactPolicy,
    check_semantics,
    default_contact_policy,
    parse_timestamp,
)

INPUT_GRAPH_PATH = CONTRACTS_DIR / "artifact-input-graph.yaml"
RESEARCH_TYPES = frozenset({"BrandResearch", "CreatorTruthPack"})


class InputGraphError(Exception):
    pass


@dataclass(frozen=True)
class InputGraph:
    version: str
    allowed: Mapping[str, frozenset[str]]
    required: Mapping[str, frozenset[str]]
    min_inputs: Mapping[str, int]


def load_input_graph(
    path: Path = INPUT_GRAPH_PATH, registry: SchemaRegistry | None = None
) -> InputGraph:
    registry = registry or default_registry()
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    types = data.get("types") if isinstance(data, dict) else None
    if not isinstance(types, dict):
        raise InputGraphError(f"{path}: missing 'types' mapping")
    if set(types) != set(registry.pipeline_types):
        raise InputGraphError(
            f"graph types {sorted(types)} != pipeline schemas {sorted(registry.pipeline_types)}"
        )
    allowed: dict[str, frozenset[str]] = {}
    required: dict[str, frozenset[str]] = {}
    min_inputs: dict[str, int] = {}
    for name, spec in types.items():
        allowed[name] = frozenset(spec.get("allowed", []))
        required[name] = frozenset(spec.get("required", []))
        min_inputs[name] = int(spec.get("min_inputs", 0))
        unknown = (allowed[name] | required[name]) - set(registry.pipeline_types)
        if unknown:
            raise InputGraphError(f"{name}: unknown types {sorted(unknown)}")
        if not required[name] <= allowed[name]:
            raise InputGraphError(f"{name}: required types must also be allowed")
        if "OutcomeRecord" in allowed[name]:
            raise InputGraphError(f"{name}: OutcomeRecord may never be an input")
    return InputGraph(str(data.get("graph_version")), allowed, required, min_inputs)


@functools.cache
def default_input_graph() -> InputGraph:
    return load_input_graph()


def stop_reason(artifact: Mapping[str, Any]) -> str | None:
    """Return the stop outcome an artifact declares, if any."""
    kind = artifact["artifact_type"]
    if kind == "LeadTriage" and artifact["triage_outcome"] != "PROCEED":
        return f"triage {artifact['triage_outcome']}"
    if kind == "BrandResearch" and artifact["research_outcome"] != "SUFFICIENT":
        return artifact["research_outcome"]
    if kind == "AnaBrandFit" and artifact["fit_outcome"] in (
        "NO_FIT",
        "INSUFFICIENT_EVIDENCE",
        "CONFLICTING_EVIDENCE",
    ):
        return artifact["fit_outcome"]
    if kind == "CommercialCheck" and artifact["status"] == "NOT_VIABLE":
        return "COMMERCIAL_NOT_VIABLE"
    if kind == "ContactProfile" and artifact["contact_outcome"] == "CONTACT_NOT_READY":
        return "CONTACT_NOT_READY"
    return None


class _Chain:
    def __init__(
        self,
        artifacts: Sequence[Any],
        now: datetime | None,
        registry: SchemaRegistry,
        policy: ContactPolicy,
        graph: InputGraph,
    ) -> None:
        self.now = now
        self.registry = registry
        self.policy = policy
        self.graph = graph
        self.findings: list[Finding] = []
        self.index: dict[str, dict[str, Any]] = {}
        self.valid: set[str] = set()
        self.cyclic: set[str] = set()
        self.ambiguous: set[str] = set()
        self._ancestors: dict[str, frozenset[str]] = {}
        self._load(artifacts)

    def add(self, code: str, artifact_id: str | None, path: str, message: str) -> None:
        self.findings.append(Finding(code, artifact_id, path, message))

    # -- indexing ------------------------------------------------------------------------

    def _load(self, artifacts: Sequence[Any]) -> None:
        ids = Counter(a.get("artifact_id") for a in artifacts if isinstance(a, dict))
        duplicates_reported: set[str] = set()
        for artifact in artifacts:
            schema_findings = self.registry.validate_artifact(artifact)
            self.findings.extend(schema_findings)
            if not isinstance(artifact, dict):
                continue
            aid = artifact.get("artifact_id")
            if not isinstance(aid, str) or artifact.get("artifact_type") not in (
                self.registry.pipeline_types
            ):
                continue
            if ids[aid] > 1:
                # Fail-closed: neither copy is trusted; dependents see a dangling reference.
                if aid not in duplicates_reported:
                    duplicates_reported.add(aid)
                    self.add(
                        F.CHAIN_DUPLICATE_ARTIFACT_ID, aid, "/artifact_id", "duplicate artifact id"
                    )
                continue
            inputs = artifact.get("input_artifact_ids")
            if not isinstance(inputs, list) or not all(isinstance(i, str) for i in inputs):
                continue
            self.index[aid] = artifact
            if not schema_findings:
                self.valid.add(aid)
                # Expiry is evaluated chain-wide below: a consumed permission is judged at
                # send time.
                semantic = check_semantics(artifact, now=None, policy=self.policy)
                self.findings.extend(semantic)
                if any(f.code == F.SEM_DUPLICATE_ID for f in semantic):
                    # Ambiguous ids make every reference into this artifact unreliable.
                    self.ambiguous.add(aid)

    def inputs_of(self, aid: str) -> list[str]:
        return [i for i in self.index[aid]["input_artifact_ids"] if i in self.index]

    def input_of_type(self, aid: str, kind: str) -> dict[str, Any] | None:
        """The unique schema-valid input of ``kind``; None if absent, ambiguous or invalid."""
        matches = [i for i in self.inputs_of(aid) if self.index[i]["artifact_type"] == kind]
        if len(matches) != 1 or matches[0] not in self.valid:
            return None
        return self.index[matches[0]]

    def ancestors(self, aid: str) -> frozenset[str]:
        if aid in self._ancestors:
            return self._ancestors[aid]
        result: set[str] = set()
        stack = list(self.inputs_of(aid))
        while stack:
            current = stack.pop()
            if current in result or current == aid:
                continue
            result.add(current)
            stack.extend(self.inputs_of(current))
        self._ancestors[aid] = frozenset(result)
        return self._ancestors[aid]

    def ancestor_of_type(self, aid: str, kind: str) -> dict[str, Any] | None:
        matches = [
            a
            for a in self.ancestors(aid)
            if self.index[a]["artifact_type"] == kind and a in self.valid
        ]
        return self.index[matches[0]] if len(matches) == 1 else None

    # -- structural graph rules ----------------------------------------------------------

    def check_graph(self) -> None:
        for aid, artifact in self.index.items():
            kind = artifact["artifact_type"]
            declared = artifact["input_artifact_ids"]
            for position, ref in enumerate(declared):
                if ref not in self.index:
                    self.add(
                        F.CHAIN_DANGLING_REFERENCE,
                        aid,
                        f"/input_artifact_ids/{position}",
                        f"input {ref!r} is not an artifact in this chain",
                    )
            types = Counter(self.index[i]["artifact_type"] for i in declared if i in self.index)
            for input_type, count in sorted(types.items()):
                if input_type not in self.graph.allowed[kind]:
                    self.add(
                        F.CHAIN_ILLEGAL_INPUT_TYPE,
                        aid,
                        "/input_artifact_ids",
                        f"{kind} may not take {input_type} as input",
                    )
                elif count > 1:
                    self.add(
                        F.CHAIN_AMBIGUOUS_INPUT,
                        aid,
                        "/input_artifact_ids",
                        f"{kind} takes at most one {input_type}",
                    )
            for missing in sorted(self.graph.required[kind] - set(types)):
                self.add(
                    F.CHAIN_MISSING_REQUIRED_INPUT,
                    aid,
                    "/input_artifact_ids",
                    f"{kind} requires a {missing} input",
                )
            if len(declared) < self.graph.min_inputs[kind]:
                self.add(
                    F.CHAIN_MISSING_REQUIRED_INPUT,
                    aid,
                    "/input_artifact_ids",
                    f"{kind} requires at least {self.graph.min_inputs[kind]} input(s)",
                )
        self._check_cycles()

    def _check_cycles(self) -> None:
        # Tarjan's strongly connected components over input edges.
        counter = 0
        stack: list[str] = []
        on_stack: set[str] = set()
        low: dict[str, int] = {}
        order: dict[str, int] = {}

        def visit(node: str) -> None:
            nonlocal counter
            order[node] = low[node] = counter
            counter += 1
            stack.append(node)
            on_stack.add(node)
            for nxt in self.inputs_of(node):
                if nxt not in order:
                    visit(nxt)
                    low[node] = min(low[node], low[nxt])
                elif nxt in on_stack:
                    low[node] = min(low[node], order[nxt])
            if low[node] == order[node]:
                component = []
                while True:
                    member = stack.pop()
                    on_stack.discard(member)
                    component.append(member)
                    if member == node:
                        break
                if len(component) > 1 or node in self.inputs_of(node):
                    members = sorted(component)
                    self.cyclic.update(members)
                    self.add(
                        F.CHAIN_CYCLE,
                        members[0],
                        "/input_artifact_ids",
                        f"artifact dependency cycle: {' -> '.join(members)}",
                    )

        for node in sorted(self.index):
            if node not in order:
                visit(node)

    # -- identity isolation --------------------------------------------------------------

    def check_run_ids(self) -> None:
        """One chain = one materialized run: every pipeline artifact shares one ``run_id``.

        The chain's run is the unique most common run id; artifacts carrying any other id
        are reported. Without a unique most common run id no run is trusted and every
        artifact is reported (fail closed).
        """
        runs = {aid: self.index[aid]["run_id"] for aid in sorted(self.valid)}
        ranked = Counter(runs.values()).most_common()
        if len(ranked) <= 1:
            return
        expected = ranked[0][0] if ranked[0][1] > ranked[1][1] else None
        for aid, run_id in runs.items():
            if expected is None:
                message = (
                    f"run_id {run_id!r}; chain mixes runs {sorted(set(runs.values()))} "
                    "with no unique chain run"
                )
            elif run_id != expected:
                message = f"run_id {run_id!r} differs from the chain's run_id {expected!r}"
            else:
                continue
            self.add(F.CHAIN_RUN_ID_MISMATCH, aid, "/run_id", message)

    @staticmethod
    def _brand_id(artifact: Mapping[str, Any]) -> str:
        if artifact["artifact_type"] == "LeadTriage":
            return artifact["brand"]["brand_id"]
        return artifact["brand_id"]

    def check_brand_ids(self, aid: str, artifact: Mapping[str, Any]) -> None:
        """BrandResearch and ContactProfile describe the Brand of the inputs they consume."""
        own = self._brand_id(artifact)
        for kind in ("LeadTriage", "BrandResearch"):
            upstream = self.input_of_type(aid, kind)
            if upstream is None:
                continue
            other = self._brand_id(upstream)
            if other != own:
                self.add(
                    F.CHAIN_BRAND_ID_MISMATCH,
                    aid,
                    "/brand_id",
                    f"brand_id {own!r} differs from {kind} {upstream['artifact_id']!r} "
                    f"brand_id {other!r}",
                )

    # -- content rules -------------------------------------------------------------------

    def visible_claims(self, aid: str) -> dict[str, tuple[dict[str, Any], str]]:
        claims: dict[str, tuple[dict[str, Any], str]] = {}
        for ancestor in self.ancestors(aid):
            artifact = self.index[ancestor]
            if artifact["artifact_type"] in RESEARCH_TYPES and ancestor in self.valid:
                for claim in artifact["claims"]:
                    claims[claim["claim_id"]] = (claim, artifact["artifact_type"])
        return claims

    def check_claim_uniqueness(self) -> None:
        owners: dict[str, list[str]] = {}
        for aid in sorted(self.valid):
            artifact = self.index[aid]
            if artifact["artifact_type"] in RESEARCH_TYPES:
                for claim in artifact["claims"]:
                    owners.setdefault(claim["claim_id"], []).append(aid)
        for claim_id, artifact_ids in sorted(owners.items()):
            if len(set(artifact_ids)) > 1:
                self.add(
                    F.CHAIN_DUPLICATE_CLAIM_ID,
                    artifact_ids[1],
                    "/claims",
                    f"claim id {claim_id!r} defined in several artifacts: "
                    f"{sorted(set(artifact_ids))}",
                )

    def _resolve_claims(
        self, aid: str, path: str, claim_ids: Sequence[str]
    ) -> list[tuple[str, dict[str, Any], str]]:
        visible = self.visible_claims(aid)
        resolved = []
        for position, claim_id in enumerate(claim_ids):
            if claim_id not in visible:
                self.add(
                    F.CHAIN_UNRESOLVED_CLAIM,
                    aid,
                    f"{path}/{position}",
                    f"claim {claim_id!r} is not defined in this artifact's evidence ancestry",
                )
                continue
            claim, owner_type = visible[claim_id]
            resolved.append((claim_id, claim, owner_type))
        return resolved

    def _check_used_claims(
        self, aid: str, path: str, claim_ids: Sequence[str], *, as_support: bool
    ) -> list[tuple[str, dict[str, Any], str]]:
        resolved = self._resolve_claims(aid, path, claim_ids)
        for claim_id, claim, _ in resolved:
            if as_support and claim["epistemic_status"] == "UNKNOWN":
                self.add(
                    F.CHAIN_UNKNOWN_AS_SUPPORT,
                    aid,
                    path,
                    f"UNKNOWN claim {claim_id!r} cannot support a hypothesis or strategy",
                )
            if claim["material"] and claim["conflict"]["status"] == "UNRESOLVED":
                self.add(
                    F.CHAIN_UNRESOLVED_CONFLICT,
                    aid,
                    path,
                    f"used claim {claim_id!r} has an unresolved material conflict (INTEL-004)",
                )
        return resolved

    def check_stops(self, aid: str) -> None:
        artifact = self.index[aid]
        if artifact["artifact_type"] == "OutcomeRecord":
            return
        for ancestor in sorted(self.ancestors(aid)):
            if ancestor not in self.valid:
                continue
            reason = stop_reason(self.index[ancestor])
            if reason is None:
                continue
            code = (
                F.CHAIN_CONTACT_NOT_READY
                if reason == "CONTACT_NOT_READY"
                else F.CHAIN_AFTER_STOP_OUTCOME
            )
            self.add(
                code,
                aid,
                "/input_artifact_ids",
                f"{artifact['artifact_type']} follows stop outcome {reason} of {ancestor}",
            )

    def check_contact_profile(self, aid: str, artifact: Mapping[str, Any]) -> None:
        research = self.input_of_type(aid, "BrandResearch")
        if research is None:
            return
        sources = {s["source_id"] for s in research["sources"]}
        for index, contact in enumerate(artifact["contacts"]):
            for sid in contact["source_ids"]:
                if sid not in sources:
                    self.add(
                        F.CHAIN_UNRESOLVED_SOURCE,
                        aid,
                        f"/contacts/{index}/source_ids",
                        f"source {sid!r} not found in input BrandResearch",
                    )

    def check_fit(self, aid: str, artifact: Mapping[str, Any]) -> None:
        for index, dimension in enumerate(artifact["dimensions"]):
            self._resolve_claims(aid, f"/dimensions/{index}/claim_ids", dimension["claim_ids"])
        self._resolve_claims(
            aid,
            "/strongest_counterargument/claim_ids",
            artifact["strongest_counterargument"]["claim_ids"],
        )

    def check_hypotheses(self, aid: str, artifact: Mapping[str, Any]) -> None:
        for index, hypothesis in enumerate(artifact["hypotheses"]):
            path = f"/hypotheses/{index}/claim_ids"
            resolved = self._check_used_claims(aid, path, hypothesis["claim_ids"], as_support=True)
            if len(resolved) != len(hypothesis["claim_ids"]):
                continue
            grounded = any(
                owner == "BrandResearch"
                and claim["epistemic_status"] in ("FACT", "SUPPORTED_INFERENCE")
                for _, claim, owner in resolved
            )
            if not grounded:
                self.add(
                    F.CHAIN_HYPOTHESIS_NOT_BRAND_GROUNDED,
                    aid,
                    path,
                    "hypothesis cites no FACT/SUPPORTED_INFERENCE claim from BrandResearch "
                    "(INTEL-009)",
                )

    def check_strategy(self, aid: str, artifact: Mapping[str, Any]) -> None:
        hypotheses = self.input_of_type(aid, "CollaborationHypothesis")
        if hypotheses is not None and artifact["selected_hypothesis_id"] not in {
            h["hypothesis_id"] for h in hypotheses["hypotheses"]
        }:
            self.add(
                F.CHAIN_UNRESOLVED_REFERENCE,
                aid,
                "/selected_hypothesis_id",
                "selected hypothesis not found in input CollaborationHypothesis",
            )
        contacts = self.input_of_type(aid, "ContactProfile")
        if (
            contacts is not None
            and artifact["target_contact_id"] != contacts["selected_contact_id"]
        ):
            self.add(
                F.CHAIN_CONTACT_MISMATCH,
                aid,
                "/target_contact_id",
                "target contact is not the ContactProfile's selected contact",
            )
        self._check_used_claims(aid, "/key_claim_ids", artifact["key_claim_ids"], as_support=True)

    def check_draft(self, aid: str, artifact: Mapping[str, Any]) -> None:
        visible = self.visible_claims(aid)
        for index, usage in enumerate(artifact["claim_usage"]):
            path = f"/claim_usage/{index}"
            claim_id = usage["claim_id"]
            if claim_id not in visible:
                self.add(
                    F.CHAIN_UNRESOLVED_CLAIM,
                    aid,
                    path,
                    f"claim {claim_id!r} is not defined in this draft's evidence ancestry",
                )
                continue
            claim, _ = visible[claim_id]
            status = claim["epistemic_status"]
            framing = usage["framing"]
            if status == "UNKNOWN" or (status != "FACT" and framing == "ASSERTED"):
                self.add(
                    F.CHAIN_ILLEGAL_EXTERNAL_FRAMING,
                    aid,
                    path,
                    f"{status} claim {claim_id!r} may not be used with framing {framing}",
                )
            if claim["material"] and claim["conflict"]["status"] == "UNRESOLVED":
                self.add(
                    F.CHAIN_UNRESOLVED_CONFLICT,
                    aid,
                    path,
                    f"used claim {claim_id!r} has an unresolved material conflict (INTEL-004)",
                )
        strategy = self.input_of_type(aid, "OutreachStrategy")
        if (
            strategy is not None
            and strategy["target_contact_id"] != artifact["recipient"]["contact_id"]
        ):
            self.add(
                F.CHAIN_CONTACT_MISMATCH,
                aid,
                "/recipient/contact_id",
                "recipient is not the strategy's target contact",
            )
        profile = self.ancestor_of_type(aid, "ContactProfile")
        if profile is not None:
            contact = next(
                (
                    c
                    for c in profile["contacts"]
                    if c["contact_id"] == artifact["recipient"]["contact_id"]
                ),
                None,
            )
            if contact is None or contact["email"] != artifact["recipient"]["email"]:
                self.add(
                    F.CHAIN_CONTACT_MISMATCH,
                    aid,
                    "/recipient/email",
                    "recipient address does not match the ContactProfile contact",
                )

    def _actual_hash(self, aid: str) -> str | None:
        draft = self.input_of_type(aid, "EmailDraft")
        return compute_draft_hash(draft) if draft is not None else None

    def check_qa(self, aid: str, artifact: Mapping[str, Any]) -> None:
        actual = self._actual_hash(aid)
        if actual is not None and artifact["draft_hash"] != actual:
            self.add(
                F.CHAIN_DRAFT_HASH_MISMATCH,
                aid,
                "/draft_hash",
                "QA report is bound to a different send_payload than the input draft",
            )

    def check_approval(self, aid: str, artifact: Mapping[str, Any]) -> None:
        if artifact["decision"] != "APPROVED":
            return
        actual = self._actual_hash(aid)
        if actual is not None and artifact["approved_draft_hash"] != actual:
            self.add(
                F.CHAIN_DRAFT_HASH_MISMATCH,
                aid,
                "/approved_draft_hash",
                "approval is bound to a different send_payload than the current draft (OPS-003)",
            )
        qa = self.input_of_type(aid, "QAGateReport")
        if qa is not None and qa["overall"] != "READY_FOR_HUMAN_REVIEW":
            self.add(
                F.CHAIN_QA_NOT_READY,
                aid,
                "/decision",
                "draft approved although QA is NOT_READY (COMP-003)",
            )

    def check_permission(self, aid: str, artifact: Mapping[str, Any]) -> None:
        bindings = artifact["bindings"]
        gates = artifact["gates"]
        draft = self.input_of_type(aid, "EmailDraft")
        approval = self.input_of_type(aid, "HumanApproval")
        qa = self.input_of_type(aid, "QAGateReport")
        profile = self.input_of_type(aid, "ContactProfile")
        for key, bound in (
            ("draft_artifact_id", draft),
            ("approval_artifact_id", approval),
            ("qa_report_artifact_id", qa),
            ("contact_profile_artifact_id", profile),
        ):
            if bound is not None and bindings[key] != bound["artifact_id"]:
                self.add(
                    F.CHAIN_BINDING_MISMATCH,
                    aid,
                    f"/bindings/{key}",
                    f"binding does not name the actual input {bound['artifact_id']!r}",
                )
        actual_hash = compute_draft_hash(draft) if draft is not None else None
        if actual_hash is not None and bindings["draft_hash"] != actual_hash:
            self.add(
                F.CHAIN_DRAFT_HASH_MISMATCH,
                aid,
                "/bindings/draft_hash",
                "permission is bound to a different send_payload than the current draft",
            )
        if draft is not None and bindings["contact_id"] != draft["recipient"]["contact_id"]:
            self.add(
                F.CHAIN_CONTACT_MISMATCH,
                aid,
                "/bindings/contact_id",
                "bound contact is not the recipient",
            )
        contact = None
        if profile is not None:
            contact = next(
                (c for c in profile["contacts"] if c["contact_id"] == bindings["contact_id"]), None
            )
            if contact is None:
                self.add(
                    F.CHAIN_CONTACT_MISMATCH,
                    aid,
                    "/bindings/contact_id",
                    "bound contact not found in input ContactProfile",
                )
        mirrors = [
            ("approval", approval["decision"] if approval else None),
            ("qa", qa["overall"] if qa else None),
            ("contact_readiness", self.policy.effective_readiness(contact) if contact else None),
        ]
        for gate, actual in mirrors:
            if actual is not None and gates[gate] != actual:
                self.add(
                    F.CHAIN_GATE_MISMATCH,
                    aid,
                    f"/gates/{gate}",
                    f"gate says {gates[gate]} but the bound input says {actual}",
                )
        if not artifact["send_authorized"]:
            return
        if approval is not None:
            if approval["decision"] != "APPROVED":
                self.add(
                    F.CHAIN_APPROVAL_NOT_APPROVED,
                    aid,
                    "/bindings/approval_artifact_id",
                    f"bound approval decision is {approval['decision']}",
                )
            elif actual_hash is not None and approval["approved_draft_hash"] != actual_hash:
                self.add(
                    F.CHAIN_DRAFT_HASH_MISMATCH,
                    aid,
                    "/bindings/approval_artifact_id",
                    "approved hash differs from the current draft's send_payload hash",
                )
        if qa is not None and qa["overall"] != "READY_FOR_HUMAN_REVIEW":
            self.add(
                F.CHAIN_QA_NOT_READY, aid, "/bindings/qa_report_artifact_id", "QA is NOT_READY"
            )
        if contact is not None and self.policy.effective_readiness(contact) != "ELIGIBLE_FOR_GATES":
            self.add(
                F.CHAIN_CONTACT_NOT_ELIGIBLE,
                aid,
                "/bindings/contact_id",
                "bound contact is not ELIGIBLE_FOR_GATES under the contact policy",
            )
        consumed = any(
            other["artifact_type"] == "SendReceipt" and aid in other["input_artifact_ids"]
            for other in self.index.values()
        )
        if (
            self.now is not None
            and not consumed
            and self.now >= parse_timestamp(artifact["expires_at"])
        ):
            self.add(
                F.SEM_SEND_PERMISSION_EXPIRED,
                aid,
                "/expires_at",
                f"unconsumed permission expired at {artifact['expires_at']}",
            )

    def check_receipt(self, aid: str, artifact: Mapping[str, Any]) -> None:
        permission = self.input_of_type(aid, "SendPermission")
        if permission is None:
            return
        if artifact["send_permission_id"] != permission["artifact_id"]:
            self.add(
                F.CHAIN_BINDING_MISMATCH,
                aid,
                "/send_permission_id",
                "send_permission_id does not name the input SendPermission",
            )
        if not permission["send_authorized"]:
            self.add(
                F.CHAIN_SEND_WITHOUT_AUTHORIZATION,
                aid,
                "/send_permission_id",
                "receipt for a permission with send_authorized=false",
            )
        sent = parse_timestamp(artifact["sent_at"])
        if not (
            parse_timestamp(permission["issued_at"])
            <= sent
            < parse_timestamp(permission["expires_at"])
        ):
            self.add(
                F.CHAIN_SEND_OUTSIDE_PERMISSION_WINDOW,
                aid,
                "/sent_at",
                "sent outside the permission's [issued_at, expires_at) window",
            )
        if artifact["draft_hash"] != permission["bindings"]["draft_hash"]:
            self.add(
                F.CHAIN_DRAFT_HASH_MISMATCH,
                aid,
                "/draft_hash",
                "sent payload hash differs from the permitted draft hash",
            )

    def check_reply(self, aid: str, artifact: Mapping[str, Any]) -> None:
        receipt = self.input_of_type(aid, "SendReceipt")
        if receipt is not None and parse_timestamp(artifact["reply_received_at"]) < parse_timestamp(
            receipt["sent_at"]
        ):
            self.add(
                F.CHAIN_TEMPORAL_ORDER, aid, "/reply_received_at", "reply received before the send"
            )

    def run(self) -> list[Finding]:
        self.check_graph()
        self.check_run_ids()
        self.check_claim_uniqueness()
        handlers = {
            "ContactProfile": self.check_contact_profile,
            "AnaBrandFit": self.check_fit,
            "CollaborationHypothesis": self.check_hypotheses,
            "OutreachStrategy": self.check_strategy,
            "EmailDraft": self.check_draft,
            "QAGateReport": self.check_qa,
            "HumanApproval": self.check_approval,
            "SendPermission": self.check_permission,
            "SendReceipt": self.check_receipt,
            "ReplyHandoff": self.check_reply,
        }
        for aid in sorted(self.valid - self.cyclic):
            if not self.ancestors(aid) <= self.valid - self.ambiguous:
                # An upstream artifact failed its schema or has duplicate ids; that finding
                # already fails the chain, and content checks against it would only add noise.
                continue
            artifact = self.index[aid]
            self.check_stops(aid)
            if artifact["artifact_type"] in ("BrandResearch", "ContactProfile"):
                self.check_brand_ids(aid, artifact)
            handler = handlers.get(artifact["artifact_type"])
            if handler is not None:
                handler(aid, artifact)
        return sorted(set(self.findings))


def validate_chain(
    artifacts: Sequence[Any],
    *,
    now: datetime | None = None,
    registry: SchemaRegistry | None = None,
    policy: ContactPolicy | None = None,
    graph: InputGraph | None = None,
) -> list[Finding]:
    """Validate all artifacts of one chain. Empty list = consistent (not authorized)."""
    registry = registry or default_registry()
    return _Chain(
        artifacts,
        now,
        registry,
        policy or default_contact_policy(),
        graph or default_input_graph(),
    ).run()

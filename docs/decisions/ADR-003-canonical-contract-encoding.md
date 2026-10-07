# ADR-003: Canonical contract encoding

**Status:** Accepted (human decisions D1–D4, 2026-10-07)

**Builds on:** ADR-001 (two generative skills, deterministic controls) and ADR-002 (structured
intermediate artifacts, deterministic send boundary). Neither is reversed.

## Context

ADR-002 requires typed intermediate artifacts and a deterministic send boundary but does not fix
how they are encoded. S1 needs one concrete, offline-testable encoding so that future skills and the
deterministic runtime validate against the same contracts.

## Decision

### 1. Contract family and file layout

- JSON Schema **Draft 2020-12**, one file per contract under `contracts/schemas/`.
- `$id` = `https://schemas.ana-agents.invalid/contracts/v1/<file>`. The reserved `.invalid` TLD
  guarantees that ids never resolve on a network. All `$ref`s are relative and local.
- Shared definitions live in `common.schema.json#/$defs` (identifiers, timestamps, hash format,
  epistemic status, qualitative rating, contact dimensions, execution results).
- Executable policy/graph data: `contracts/policies/contact-policy.yaml`,
  `contracts/artifact-input-graph.yaml`.
- Every schema declares `x-ana-kind`: `pipeline`, `supporting`, `envelope`, `definitions` or `policy`.

### 2. ArtifactEnvelope composition

Every pipeline schema composes `artifact-envelope.schema.json` through `allOf` and closes the object
with `unevaluatedProperties: false`. The envelope carries `artifact_id`, `artifact_type`,
`schema_version`, `contract_version`, `produced_at`, `producer {kind, id}`, `run_id`,
`input_artifact_ids`. The envelope carries no authority: `producer` is declared data.

Draft 2020-12 discards annotations from a failing `allOf` branch, so one envelope error also produces
an `unevaluatedProperties` error listing declared fields. The registry drops that error only when the
instance has no undeclared key; a genuine extra key is still reported.

### 3. Pipeline vs supporting types

- **Pipeline artifacts** (15): `LeadTriage`, `CreatorTruthPack`, `BrandResearch`, `ContactProfile`,
  `AnaBrandFit`, `CollaborationHypothesis`, `CommercialCheck`, `OutreachStrategy`, `EmailDraft`,
  `QAGateReport`, `HumanApproval`, `SendPermission`, `SendReceipt`, `ReplyHandoff`, `OutcomeRecord`.
  They carry the envelope and are addressable by `artifact_id`.
- **Supporting structures**: `SourceRecord` and `EvidenceClaim` (embedded in `BrandResearch` /
  `CreatorTruthPack`) and `EvalCase` (eval descriptions). They have no envelope, are not artifacts,
  and therefore can never be an input of anything.
- `CreatorTruthPack` is a pipeline artifact (an input of fit and hypotheses) with no inputs of its
  own. In this repository it exists only as `SYNTHETIC_FIXTURE`.
- The registry fails construction if the envelope's `artifact_type` enum differs from the set of
  `pipeline` schemas.

### 4. Versioning

- `contract_version` (envelope `const "1.0.0"`): version of the contract family as a whole —
  envelope, input graph, hash algorithm, finding codes.
- `schema_version` (per schema `const "1.0.0"`): version of one artifact schema.
- Any breaking change bumps the relevant version; the `const` makes old/new mismatches fail closed.
- Finding codes in `src/ana_agents/contracts/findings.py` are part of the contract.

### 5. Allowed artifact-input graph

Fail-closed. Each artifact's `input_artifact_ids` may only contain the listed types, at most one per
type; listed types are also required, except `OutcomeRecord` (any listed type, at least one). The
executable source is `contracts/artifact-input-graph.yaml`; the restatement below is checked against
it by `tests/contracts/test_input_graph.py`.

<!-- input-graph:begin -->
```text
LeadTriage              <- none
CreatorTruthPack        <- none
BrandResearch           <- LeadTriage
ContactProfile          <- LeadTriage, BrandResearch
AnaBrandFit             <- BrandResearch, CreatorTruthPack
CollaborationHypothesis <- AnaBrandFit, BrandResearch, CreatorTruthPack
CommercialCheck         <- CollaborationHypothesis
OutreachStrategy        <- CollaborationHypothesis, CommercialCheck, ContactProfile
EmailDraft              <- OutreachStrategy
QAGateReport            <- EmailDraft
HumanApproval           <- EmailDraft, QAGateReport
SendPermission          <- EmailDraft, HumanApproval, QAGateReport, ContactProfile
SendReceipt             <- SendPermission
ReplyHandoff            <- SendReceipt
OutcomeRecord           <- LeadTriage, BrandResearch, ContactProfile, AnaBrandFit, CollaborationHypothesis, CommercialCheck, OutreachStrategy, EmailDraft, QAGateReport, HumanApproval, SendPermission, SendReceipt, ReplyHandoff
```
<!-- input-graph:end -->

Consequences: no type accepts `OutcomeRecord`, so outcomes cannot feed back into sending; raw
research (`BrandResearch`, `SourceRecord`) is never a direct input of `EmailDraft`, `SendPermission`
or `SendReceipt`; `ContactProfile` is not an input of `AnaBrandFit`. Claims are resolved through the
artifact's ancestry, so a draft may *reference* a research claim id in its evidence map without
taking research as an input. Cycles, dangling ids and duplicate artifact ids are rejected.

Stop outcomes — triage `DEFER`/`REJECT`, research `INSUFFICIENT_EVIDENCE`/`CONFLICTING_EVIDENCE`,
fit `NO_FIT`/`INSUFFICIENT_EVIDENCE`/`CONFLICTING_EVIDENCE`, commercial `NOT_VIABLE`, contact
`CONTACT_NOT_READY` — may only be followed by an `OutcomeRecord`.

### 6. Two-axis ContactProfile model (D3)

A contact has independent dimensions `source_class` (`official_published`, `public_found`,
`inferred`, `private`, `unknown`), `verification` (`verified`, `unverified`, `catch_all`, `unknown`)
and `public_business_context` (boolean). `readiness` (`ELIGIBLE_FOR_GATES`, `REVIEW_REQUIRED`,
`NO_SEND`) is derived by `contracts/policies/contact-policy.yaml`: every matching rule contributes,
the most restrictive readiness wins, no match means `NO_SEND`. Only
`official_published + verified + public_business_context=true` is `ELIGIBLE_FOR_GATES`. A declared
readiness may be stricter than the policy, never looser. `ELIGIBLE_FOR_GATES` is not send
authorization, compliance clearance or approval. Resolving `REVIEW_REQUIRED` is `MISSING` (future
scope).

### 7. CONTACT_NOT_READY semantics (D2, SPEC INTEL-010)

`ContactProfile.contact_outcome` is `READY_FOR_GATES` or `CONTACT_NOT_READY`. `READY_FOR_GATES`
requires a selected contact whose effective readiness is `ELIGIBLE_FOR_GATES`. `CONTACT_NOT_READY`
stops `OutreachStrategy` and everything after it. It is **not** an `AnaBrandFit` outcome: fit and
contact readiness stay independent (INTEL-007).

### 8. Draft hash semantics (D4)

Human approval and `SendPermission` bind to the exact outbound payload the recipient would receive.

- **Projection `send-payload-v1`:** `recipient {contact_id, email}`, `sender_identity_id`,
  `subject`, `body_text`, `body_html_light`, `links [{url, label}]`, plus
  `payload_version: "send-payload-v1"`.
- **Excluded:** envelope metadata (`artifact_id`, `artifact_type`, `schema_version`,
  `contract_version`, `produced_at`, `producer`, `run_id`, `input_artifact_ids`) and internal
  bookkeeping (`claim_usage`, `hash_algorithm`, `draft_hash`).
- **Canonicalization:** JSON with sorted keys, separators `(",", ":")`, `ensure_ascii=False`,
  NaN/Infinity rejected, UTF-8. Strings are hashed exactly — no whitespace, case or Unicode
  normalization — because the recipient receives exactly those code points. `links` order is
  significant.
- **Digest:** `"sha256:" + hex(sha256(bytes))`; `EmailDraft.hash_algorithm = "send-payload-v1+sha256"`.
- Validators always recompute the hash from the current draft; a stale declared hash, a QA report,
  approval, permission or receipt bound to a different hash are all rejected.
- Every `EmailDraft` field must be classified as payload or non-payload in
  `src/ana_agents/contracts/hashing.py` (test-enforced). Adding a payload field requires a new
  payload/hash version. Attachments are not representable in v1.

### 9. Schema-valid SendPermission is not authorization

`SendPermission` in S1 is a data contract plus consistency validation. A JSON object that validates
against `send-permission.schema.json` is **not** send authorization. There is no trusted issuer, no
signature and no runtime issuance; `producer.kind = runtime` is declared data, not cryptographic
proof. Issuance belongs to future trusted deterministic runtime code. The validators check that a
permission record is internally consistent (all seven gates pass when `send_authorized = true`,
block reasons present iff denied, `expires_at > issued_at`, bindings among inputs) and bound to the
actual draft hash, approval decision, QA state and contact readiness. An unconsumed authorized
permission is expired when `now >= expires_at`; a consumed one is judged by `SendReceipt.sent_at`
falling in `[issued_at, expires_at)`.

### 10. JSON Schema vs Python semantic validation

- **JSON Schema** owns shape: types, enums, `required`, closed objects, local conditional presence
  (FACT needs ≥1 source id; SUPPORTED_INFERENCE needs some support; volatile claims need
  freshness; `APPROVED` needs a hash; `stop_followups` is `true`; producer `const` for approval /
  permission / receipt).
- **Python single-artifact semantics** (`semantic.py`) own value/policy/time rules: id resolution
  inside an artifact, grounded inference, contact-policy readiness, commercial `VIABLE` without
  policy, draft hash recomputation, hard-check non-compensation, execution evidence for PASS/FAIL,
  SendPermission consistency and expiry, reply stop/classification order, producer authority
  (duplicated behind the schema `const` as defense in depth).
- **Python chain rules** (`evidence/chain.py`) own cross-artifact relations: input graph, cycles,
  dangling ids, stop outcomes, claim resolution through ancestry, external framing, unresolved
  conflicts, Brand grounding, contact/draft/approval/permission/receipt bindings.
- Semantic and chain content rules run only on schema-valid artifacts. Descendants of a
  schema-invalid artifact, or of an artifact with duplicate ids, skip content checks: the upstream
  finding already fails the chain and checks against ambiguous data would only add noise.
- Validity is never truth and never authorization.

### 11. Timestamps

`format: date-time` (RFC 3339) is asserted, not annotated: the registry runs the jsonschema
`FormatChecker` with `rfc3339-validator` / `rfc3986-validator` installed and refuses to start if a
canary shows `date-time` or `uri` checking is inactive. RFC 3339 requires an explicit offset, so
naive timestamps are rejected; non-UTC offsets are accepted (no UTC-only rule).

## Consequences

- Skills and runtime share one machine-checkable contract; drift between ADR, YAML, schema enum and
  hash field set is test-detected.
- S1 proves contract consistency only. It does not prove research truth, model behaviour, legal
  compliance or send authority.

## Revisit conditions

- A canonical requirement needs an input edge the graph does not allow (stop and amend this ADR).
- The EmailDraft sendable-field set changes (new hash version).
- A trusted runtime issuer / signature for `SendPermission` is introduced (new ADR).
- A review mechanism for `REVIEW_REQUIRED` contacts is authorized.

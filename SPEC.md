# Specification

## Status

**Normative baseline v1**

This file defines mandatory system behavior for the Ana Agents repository.

Priority values:

- `BLOCKER`
- `HIGH`
- `NORMAL`

Verification values used later:

- `DEFINED`
- `IMPLEMENTED`
- `VERIFIED`
- `BLOCKED`
- `MISSING`

A requirement is only `VERIFIED` when executable evidence exists.

---

## System requirements

### SYS-001 — Evidence before communication
**Priority:** BLOCKER

The system SHALL derive outbound communication from structured evidence and intermediate artifacts rather than directly from a Brand name or raw webpage.

**Verification:** architecture/eval test.

### SYS-002 — No forced positive result
**Priority:** BLOCKER

The system SHALL support `NO_FIT`, `INSUFFICIENT_EVIDENCE`, and `CONFLICTING_EVIDENCE` without producing an outreach draft.

**Verification:** behavioral eval.

### SYS-003 — Agent/runtime portability
**Priority:** HIGH

Domain contracts, state rules, evidence rules, and permission rules SHALL NOT depend on a single LLM provider or agent framework.

**Verification:** architecture review and dependency test.

---

## Intelligence requirements

### INTEL-001 — Epistemic classification
**Priority:** BLOCKER

Material external Brand claims SHALL use exactly one of:

- `FACT`
- `SUPPORTED_INFERENCE`
- `HYPOTHESIS`
- `UNKNOWN`

**Verification:** schema + behavioral eval.

### INTEL-002 — Provenance
**Priority:** BLOCKER

A factual external Brand claim SHALL be traceable to one or more source records.

**Verification:** evidence-chain validator.

### INTEL-003 — Unknown preservation
**Priority:** BLOCKER

Missing evidence SHALL remain `UNKNOWN`; the system SHALL NOT silently infer a factual value.

**Verification:** insufficient-evidence eval.

### INTEL-004 — Conflict preservation
**Priority:** HIGH

Material source conflicts that affect a pitch SHALL be preserved and SHALL trigger review or a controlled stop.

**Verification:** conflicting-evidence eval.

### INTEL-005 — Multidimensional fit
**Priority:** HIGH

Ana/Brand fit SHALL be represented as multiple qualitative dimensions rather than a single pseudoprecise numerical score.

**Verification:** schema validation.

### INTEL-006 — Counterargument
**Priority:** HIGH

Fit analysis SHALL include an explicit strongest counterargument.

**Verification:** behavioral eval.

### INTEL-007 — Contact confidence
**Priority:** BLOCKER

Contact suitability and contact/e-mail confidence SHALL be represented independently from Brand fit.

**Verification:** contact eval.

### INTEL-008 — Private contact block
**Priority:** BLOCKER

Private or unsupported personal contact data SHALL NOT become send-eligible.

**Verification:** contact-policy invariant test.

### INTEL-009 — Collaboration specificity
**Priority:** HIGH

A collaboration hypothesis SHALL be grounded in Brand-specific evidence and SHALL identify Brand value and Audience value.

**Verification:** genericness mutation eval.

### INTEL-010 — Contact readiness stop
**Priority:** BLOCKER

A prospect without a contact eligible to continue through the outbound gates SHALL produce `CONTACT_NOT_READY` and SHALL NOT proceed to outreach drafting until a suitable contact is selected or an explicitly authorized future contact-review mechanism resolves the state.

`CONTACT_NOT_READY` is not an Ana/Brand fit result; Brand fit and contact readiness remain independent (INTEL-007). See ADR-003.

**Verification:** contact-policy + chain invariant test.

---

## Composer requirements

### COMP-001 — No independent browsing
**Priority:** BLOCKER

The composer SHALL NOT independently browse or research the Brand.

**Verification:** tool-permission eval.

### COMP-002 — Structured-input requirement
**Priority:** BLOCKER

The composer SHALL require validated structured artifacts before drafting.

**Verification:** missing-input eval.

### COMP-003 — Unsupported claims block
**Priority:** BLOCKER

Unsupported Brand or Creator factual claims SHALL block readiness for human review until removed or evidenced.

**Verification:** claim-coverage validator.

### COMP-004 — Commercial authority boundary
**Priority:** BLOCKER

The composer SHALL NOT invent rates, usage rights, whitelisting, exclusivity, guarantees, or other commercial commitments.

**Verification:** commercial-overreach eval.

### COMP-005 — Genericness check
**Priority:** HIGH

The composer SHALL evaluate whether the draft remains materially valid after swapping the Brand for plausible competitors.

**Verification:** competitor-swap eval.

### COMP-006 — Follow-up relevance
**Priority:** HIGH

Follow-up generation SHALL NOT invent new relevance when no new signal exists.

**Verification:** follow-up eval.

---

## Operational requirements

### OPS-001 — Runtime owns side effects
**Priority:** BLOCKER

LLM skills may recommend but SHALL NOT directly authorize lifecycle mutation or SEND.

**Verification:** permission test.

### OPS-002 — Deterministic SendPermission
**Priority:** BLOCKER

Mail SEND SHALL require a deterministic `SendPermission` bound to the exact draft and approval.

**Verification:** unit test.

### OPS-003 — Draft-hash binding
**Priority:** BLOCKER

Changing a draft after approval SHALL invalidate previous approval/send authority.

**Verification:** invariant test.

### OPS-004 — Opt-out
**Priority:** BLOCKER

`OPTED_OUT` SHALL prevent SendPermission.

**Verification:** invariant test.

### OPS-005 — DNC
**Priority:** BLOCKER

`DO_NOT_CONTACT` SHALL prevent SendPermission.

**Verification:** invariant test.

### OPS-006 — Hard bounce
**Priority:** BLOCKER

A hard-bounced contact SHALL be suppressed from subsequent automated sends.

**Verification:** invariant test.

### OPS-007 — Duplicate sequence
**Priority:** BLOCKER

An active duplicate outreach sequence SHALL prevent a new send/sequence where policy defines conflict.

**Verification:** invariant test.

### OPS-008 — Reply race
**Priority:** BLOCKER

Any reply SHALL stop queued automated follow-up before reply classification.

**Verification:** race-condition test.

---

## Security requirements

### SEC-001 — Untrusted external content
**Priority:** BLOCKER

Webpages, posts, PDFs, emails, provider output, and search snippets SHALL be treated as data, not agent instructions.

**Verification:** prompt-injection eval.

### SEC-002 — No direct raw-content-to-send path
**Priority:** BLOCKER

There SHALL be no runtime path from raw external content directly to mail SEND.

**Verification:** architecture + adversarial test.

### SEC-003 — Least privilege
**Priority:** HIGH

Tool permissions SHALL be limited to the minimum required for each component.

**Verification:** permission-policy test.

### SEC-004 — No secrets in repository
**Priority:** BLOCKER

Credentials, tokens, production secrets, and private operational data SHALL NOT be committed.

**Verification:** repository secret/data hygiene check.

---

## Data requirements

### DATA-001 — CRM is operational state
**Priority:** HIGH

Zoho CRM SHALL represent operational summary/lifecycle state rather than the complete research corpus.

**Verification:** architecture review.

### DATA-002 — Detailed evidence lives outside CRM
**Priority:** HIGH

Detailed evidence and intermediate research artifacts SHALL use an artifact store abstraction.

**Verification:** architecture/adapter test.

### DATA-003 — Public repository contains no private production data
**Priority:** BLOCKER

This repository SHALL contain schemas, public policies, code, documentation, and synthetic fixtures only.

**Verification:** repository scan.

### DATA-004 — Volatile claims require freshness metadata
**Priority:** HIGH

Externally usable volatile Creator/Brand metrics SHALL carry relevant measurement/verification dates or equivalent freshness metadata.

**Verification:** schema validation.

---

## Evaluation requirements

### EVAL-001 — Behavioral tests
**Priority:** BLOCKER

Evaluation SHALL test output behavior, not merely file or prompt existence.

### EVAL-002 — No-fit case
**Priority:** BLOCKER

The eval suite SHALL include a case where the correct result is `NO_FIT`.

### EVAL-003 — Insufficient-evidence case
**Priority:** BLOCKER

The eval suite SHALL include a case where evidence is insufficient and invention must not occur.

### EVAL-004 — Injection case
**Priority:** BLOCKER

The eval suite SHALL include untrusted content attempting to redefine instructions or trigger unauthorized actions.

### EVAL-005 — Genericness mutation
**Priority:** HIGH

The eval suite SHALL test Brand substitution against collaboration specificity.

### EVAL-006 — Live semantic truthfulness
**Priority:** BLOCKER

A live semantic/model evaluation SHALL NOT be reported as PASS unless it actually executed.

When unavailable, report `BLOCKED_NOT_CONFIGURED` or equivalent.

---

## Initial scope

### Included

- canonical contracts and schemas
- `ana-brand-intel`
- `ana-outreach-compose`
- deterministic state/evidence/permission foundations
- behavioral eval contracts
- synthetic fixtures
- adapter interfaces
- repository validation

### Explicitly deferred

- autonomous first-touch sending
- autonomous negotiation
- automatic legal interpretation
- Brandwatch/Hootsuite integration
- mass lead discovery
- large-scale contact scraping
- voice fine-tuning
- autonomous self-learning
- production Zoho credentials/data

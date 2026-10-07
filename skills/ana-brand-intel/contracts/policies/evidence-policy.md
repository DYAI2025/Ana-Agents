# Evidence Policy

**Status:** S1 contract policy. Normative basis: SPEC INTEL-001..004, INTEL-009, COMP-003,
SYS-001/002, EVAL-006. Decision record: ADR-003.

## Epistemic classes

Every material Brand/Creator claim (`EvidenceClaim`) has exactly one `epistemic_status`:

| Status | Requirement | Enforced by |
|---|---|---|
| `FACT` | at least one `source_id`; every id resolves to a `SourceRecord` in the same artifact | schema (`minItems`), semantic (`SEM_UNRESOLVED_SOURCE`) |
| `SUPPORTED_INFERENCE` | a source, or a supporting claim that is itself grounded (circular support does not count) | schema (`anyOf`), semantic (`SEM_UNSUPPORTED_INFERENCE`) |
| `HYPOTHESIS` | may be unsupported; never framed as confirmed | chain (`CHAIN_ILLEGAL_EXTERNAL_FRAMING`) |
| `UNKNOWN` | missing evidence stays here; never filled by inference | chain (`CHAIN_ILLEGAL_EXTERNAL_FRAMING`, `CHAIN_UNKNOWN_AS_SUPPORT`) |

## External framing

`EmailDraft.claim_usage` lists every claim a draft relies on with its framing:

- `ASSERTED` — allowed only for `FACT`.
- `HEDGED` / `QUESTION` — required for `SUPPORTED_INFERENCE` and `HYPOTHESIS`.
- `UNKNOWN` claims may not be used externally at all.

`claim_usage` is the evidence map, not message content; whether the text actually matches the
declared framing is a semantic quality question for the future composer eval (`MISSING` in S1).

## Grounding of collaboration hypotheses

Each hypothesis must cite at least one `FACT` or `SUPPORTED_INFERENCE` claim from `BrandResearch`
(`CHAIN_HYPOTHESIS_NOT_BRAND_GROUNDED`). Creator-only evidence is not Brand-specific.

## Conflicts

A claim's `conflict.status` is `NONE`, `UNRESOLVED` or `RESOLVED`, with the conflicting claim ids
preserved. A material claim with an `UNRESOLVED` conflict that is used by a hypothesis, strategy or
draft blocks the chain (`CHAIN_UNRESOLVED_CONFLICT`). Resolution keeps the conflicting ids and adds a
`resolution_note`; it does not delete evidence.

## Stop outcomes

`NO_FIT`, `INSUFFICIENT_EVIDENCE`, `CONFLICTING_EVIDENCE`, triage `DEFER`/`REJECT`, commercial
`NOT_VIABLE` and `CONTACT_NOT_READY` are successful outcomes. Only an `OutcomeRecord` may follow
them (`CHAIN_AFTER_STOP_OUTCOME`, `CHAIN_CONTACT_NOT_READY`).

## Validation is not truth

JSON Schema validity and a clean evidence chain mean "consistent with the contract". They do not
prove that any claim is true, that sources say what the claim says, or that sending is allowed.

## SendPermission is not authorization in S1

A JSON object that validates against `send-permission.schema.json` is **not** send authorization.
S1 has no trusted issuer and no signature; `producer.kind = runtime` is declared data. Real issuance
belongs to future trusted deterministic runtime code (ADR-002, ADR-003).

## Execution evidence

A check or eval result of `PASS` or `FAIL` requires `executed = true`, an `execution_ref` and an
`executed_at` timestamp (`SEM_EVAL_PASS_WITHOUT_EXECUTION`). A semantic/model eval that did not run
is `BLOCKED_NOT_CONFIGURED` or `NOT_RUN`, and any hard check not `PASS` forces QA `NOT_READY`
(`SEM_QA_HARD_FAIL_COMPENSATED`).

# ADR-002: Structured intermediate artifacts and deterministic send boundary

**Status:** Accepted

## Context

Raw websites, search results, CRM notes, email content, and provider results are untrusted inputs. Directly allowing those inputs to influence side-effecting tools creates both factual and prompt-injection risk.

Schema validation alone cannot prove that a claim is true, but explicit intermediate artifacts make provenance, policy, and quality independently testable.

## Decision

Adopt a structured intermediate-artifact pipeline:

```text
LeadTriage
-> BrandResearch
-> ContactProfile
-> AnaBrandFit
-> CollaborationHypothesis
-> CommercialCheck
-> OutreachStrategy
-> EmailDraft
-> QAGateReport
-> HumanApproval
-> SendPermission
-> SendReceipt
-> ReplyHandoff
-> OutcomeRecord
```

Raw external content must be transformed into structured claims and evidence records before it can influence downstream strategy.

The composer must not independently browse.

A deterministic `SendPermission` must be required before any send adapter can execute.

## Consequences

- evidence-chain validation becomes a first-class runtime responsibility
- approvals bind to exact draft content/hash
- modifying an approved draft invalidates send authority
- tests can target contracts and invariants rather than prose prompts
- missing evidence can fail closed

## Alternatives considered

### Direct model-to-mail workflow

Rejected due to untrusted-content, evidence, and authorization risks.

### Human approval alone without deterministic permission artifact

Rejected because the system also needs machine-checkable binding between approval, exact draft, suppression state, and policy state.

## Revisit conditions

Revisit only if an equivalent or stronger mechanism provides the same traceability and action-control guarantees.

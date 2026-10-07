# Domain Contract

Pinned source snapshot used for build: `DYAI2025/Ana-Agents@31580c135fe25852540bb73bed772f3bef5c5b41`.

## Canonical direct input graph

`OutreachStrategy` requires exactly: `CollaborationHypothesis`, `CommercialCheck`, `ContactProfile`.

`EmailDraft` directly consumes `OutreachStrategy` only.

`QAGateReport` directly consumes `EmailDraft` only.

Do not add transitive ancestors as illegal direct artifact inputs.

## Outputs

- OutreachStrategy
- EmailDraft
- semantic findings for runtime QAGateReport

## Authority boundary

The skill drafts only. Runtime owns schema/evidence validation, hash verification/computation, CRM lifecycle mutation, HumanApproval, SendPermission, and SEND.

# Repository Contract Bindings

Canonical repository: `DYAI2025/Ana-Agents`

When repository/runtime validation is available, bind composition to:

- `contracts/artifact-input-graph.yaml`
- `contracts/schemas/outreach-strategy.schema.json`
- `contracts/schemas/email-draft.schema.json`
- `contracts/schemas/qa-gate-report.schema.json`
- `contracts/schemas/commercial-check.schema.json`
- `contracts/policies/evidence-policy.md`
- `contracts/policies/untrusted-content-policy.md`

Canonical direct inputs remain:
- OutreachStrategy <- CollaborationHypothesis + CommercialCheck + ContactProfile
- EmailDraft <- OutreachStrategy
- QAGateReport <- EmailDraft

If repository validators are unavailable, do not claim schema, hash, chain, or QA execution passed.

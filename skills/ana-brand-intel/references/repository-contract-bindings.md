# Repository Contract Bindings

Canonical repository: `DYAI2025/Ana-Agents`

The installed skill does not embed a second competing contract family. When operating with the repository/runtime, bind to:

- `contracts/artifact-input-graph.yaml`
- `contracts/schemas/brand-research.schema.json`
- `contracts/schemas/contact-profile.schema.json`
- `contracts/schemas/ana-brand-fit.schema.json`
- `contracts/schemas/collaboration-hypothesis.schema.json`
- `contracts/schemas/evidence-claim.schema.json`
- `contracts/schemas/source-record.schema.json`
- `contracts/policies/evidence-policy.md`
- `contracts/policies/contact-policy.yaml`
- `contracts/policies/freshness-policy.md`
- `contracts/policies/untrusted-content-policy.md`

If these canonical validators are unavailable in the current runtime, the skill may still reason semantically but must not report schema, chain, or runtime validation as PASS.

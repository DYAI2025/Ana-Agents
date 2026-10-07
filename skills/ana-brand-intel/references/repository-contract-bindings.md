# Repository Contract Bindings

Canonical repository: `DYAI2025/Ana-Agents`

The installed skill does not embed a second competing contract family. It carries byte-identical pins of the canonical files; `contracts/PINS.json` lists each pin with its canonical repository path and sha256. Canonical truth always stays in the repository.

| Package file (pin) | Canonical repository path |
|---|---|
| `contracts/artifact-input-graph.yaml` | contracts/artifact-input-graph.yaml |
| `schemas/brand-research.schema.json` | contracts/schemas/brand-research.schema.json |
| `schemas/contact-profile.schema.json` | contracts/schemas/contact-profile.schema.json |
| `schemas/ana-brand-fit.schema.json` | contracts/schemas/ana-brand-fit.schema.json |
| `schemas/collaboration-hypothesis.schema.json` | contracts/schemas/collaboration-hypothesis.schema.json |
| `schemas/evidence-claim.schema.json` | contracts/schemas/evidence-claim.schema.json |
| `schemas/source-record.schema.json` | contracts/schemas/source-record.schema.json |
| `contracts/policies/evidence-policy.md` | contracts/policies/evidence-policy.md |
| `contracts/policies/contact-policy.yaml` | contracts/policies/contact-policy.yaml |
| `contracts/policies/freshness-policy.md` | contracts/policies/freshness-policy.md |
| `contracts/policies/untrusted-content-policy.md` | contracts/policies/untrusted-content-policy.md |

`contracts/PINS.json` is the complete list; this table names the files the skill reads most.

The canonical validators (`validate_chain` in the repository's `ana_agents` package) are not part of this package. If they are unavailable in the current runtime, the skill may still reason semantically but must not report schema, chain, or runtime validation as PASS.

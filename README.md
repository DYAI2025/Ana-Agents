# Ana Agents

Repository foundation for the Ana Savu agent ecosystem.

This repository is intended to hold reusable skills, deterministic runtime controls, schemas, policies, evaluations, and agent documentation for the Ana project. The first implemented domain is evidence-grounded brand-partnership outreach.

## Core principle

The system is not a generic cold-email generator.

```text
Evidence
-> Structured Understanding
-> Ana <-> Brand Fit
-> Collaboration Hypothesis
-> Commercial Check
-> Outreach Strategy
-> Draft
-> Quality Gates
-> Human Approval
-> Controlled Send
```

The email is a downstream artifact, not the starting point.

## Canonical documents

Read in this order before making material changes:

1. `AGENTS.md`
2. `SPEC.md`
3. `ARCHITECTURE.md`
4. Relevant ADRs under `docs/decisions/`
5. Relevant contracts, schemas, policies, and tests

## Planned first capabilities

- `ana-brand-intel`
- `ana-outreach-compose`
- deterministic state, evidence, policy, duplicate, suppression, and send-permission controls
- Zoho CRM/Mail adapters behind explicit interfaces
- behavioral and adversarial evaluations

## Data safety

This repository is public.

Do **not** commit production CRM exports, real private contact lists, OAuth tokens, API keys, private email threads, private rate cards, unpublished creator metrics, private travel plans, or other operationally sensitive data.

Use schemas, synthetic fixtures, `example.invalid` addresses, and explicit `MISSING` markers instead.

Raw research documents should remain outside this public repository unless explicitly reviewed and approved for publication.

## Current status

Repository foundation only. Production integrations, private Ana knowledge, legal operating policy, and live semantic-agent evaluation are not yet implemented.

See `SPEC.md` for normative requirements and `ARCHITECTURE.md` for the target design.

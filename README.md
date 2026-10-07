# Ana Agents

## Vince: use the Skills now

Direct downloads:

- [ana-brand-intel.zip](downloads/ana-brand-intel.zip)
- [ana-outreach-compose.zip](downloads/ana-outreach-compose.zip)

Setup with the existing Vince CRM Orchestrator: [docs/VINCE_START_HERE.md](docs/VINCE_START_HERE.md)

Claude-for-Chrome setup prompt: [prompts/CLAUDE_FOR_CHROME_SETUP.md](prompts/CLAUDE_FOR_CHROME_SETUP.md)


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

Slice S1 — canonical contracts and validation foundation:

- JSON Schema (Draft 2020-12) contracts for every pipeline artifact under `contracts/schemas/`
- executable contact policy (`contracts/policies/contact-policy.yaml`) and artifact input graph
  (`contracts/artifact-input-graph.yaml`); decisions in `docs/decisions/ADR-003-canonical-contract-encoding.md`
- offline schema registry, single-artifact semantic validator, cross-artifact evidence-chain
  validator and `send-payload-v1` draft hashing (`src/ana_agents/`)
- synthetic fixtures with valid chains and a negative-case manifest (`contracts/examples/`)
- requirement mapping in `docs/TRACEABILITY.md`

Not implemented: the `ana-brand-intel` / `ana-outreach-compose` skills, any runtime service
(state machine, scheduler, suppression, duplicates, SendPermission issuer), Zoho adapters, live
model evaluations, production commercial/legal policy. **Nothing in this repository grants send
authority:** a schema-valid `SendPermission` is a data record, not an authorization.

See `SPEC.md` for normative requirements and `ARCHITECTURE.md` for the target design.

## Development

Requires Python >= 3.12 and [uv](https://docs.astral.sh/uv/). Everything runs offline after `uv sync`;
tests never contact Zoho, model providers or other live services.

```bash
uv sync                                   # install declared dependencies into .venv
uv run ruff check .                       # lint
uv run ruff format --check .              # formatting
uv run pytest -q                          # tests
uv run python scripts/validate_contracts.py   # schemas, policies, examples, negative cases
uv run python scripts/check_repo_hygiene.py   # basic tracked-file hygiene (not a secret scanner)
```

Negative fixtures are mutations of the valid chains declared in
`contracts/examples/negative-cases.yaml`; each case lists the exact findings it must produce.

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

## Current generative capabilities

Two skill sources are now assembled:

- `ana-brand-intel`
- `ana-outreach-compose`

They are **not yet approved releases**. Their machine-readable release gates remain BLOCKED until exact-head deterministic validation, live semantic/model evals, independent evaluation, and Vince workspace smoke testing are actually executed.

Deterministic state, evidence, policy, duplicate, suppression, send-permission controls and production CRM/mail adapters remain separate runtime work.

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

Skill source exists for `ana-brand-intel` and `ana-outreach-compose`, but live semantic/model evaluations and approved installable releases remain blocked. Runtime services (state machine, scheduler, suppression, duplicates, trusted SendPermission issuer), Zoho adapters, and production commercial/legal policy are still not implemented.

**Nothing in this repository grants send authority:** a draft, a schema-valid `SendPermission`, or a skill output is not authorization.

For Vince/distribution:
- start with `docs/VINCE_QUICKSTART.md`;
- normal use: `docs/VINCE_DAILY_USE.md`;
- architecture in plain language: `docs/ARCHITECTURE_FOR_HUMANS.md`;
- setup automation prompt: `prompts/CLAUDE_FOR_CHROME_SETUP.md`;
- release/candidate packaging: `scripts/package_skills.py` and `scripts/verify_release.py`.

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

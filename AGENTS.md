# AGENTS.md

## Purpose

This file governs coding agents and automation working in this repository.

The project prioritizes truthfulness, traceability, maintainability, testability, portability, least privilege, controlled autonomy, and commercial usefulness.

Do not optimize for maximum automation, maximum agent count, or maximum outbound volume.

## Mandatory read order

Before any material implementation or architecture change, read:

1. `AGENTS.md`
2. `SPEC.md`
3. `ARCHITECTURE.md`
4. Relevant ADRs under `docs/decisions/`
5. Relevant skill `SKILL.md`
6. Relevant canonical contracts, schemas, policies, and tests

Do not implement from chat memory when the repository contains current project rules.

## Source-of-truth hierarchy

Use this precedence:

```text
SPEC.md
-> accepted ADRs
-> ARCHITECTURE.md
-> canonical contracts/policies
-> skill instructions
-> implementation
```

If implementation conflicts with a higher-level contract, report drift. Do not silently rewrite documentation to match code.

## Evidence labels

Use these labels when material uncertainty exists:

- `VERIFIED_FACT`
- `EVIDENCE_BACKED_RECOMMENDATION`
- `DESIGN_DECISION`
- `ASSUMPTION`
- `MISSING`
- `SOURCE_NEEDED`
- `BLOCKER`

Do not phrase assumptions as facts.

## Core architecture invariants

1. Raw external content must never have a direct path to SEND.
2. Generative models must never create send authority.
3. Hard blocks cannot be compensated by soft quality.
4. `NO_FIT`, `INSUFFICIENT_EVIDENCE`, and `CONFLICTING_EVIDENCE` are valid successful outcomes.
5. Material Brand claims use exactly: `FACT`, `SUPPORTED_INFERENCE`, `HYPOTHESIS`, `UNKNOWN`.
6. CRM operational state and full research evidence are separate concerns.
7. Skills may recommend transitions; deterministic runtime owns side effects.
8. Any reply stops automated follow-up before semantic classification.
9. Production/private data must not be committed to this public repository.
10. Missing integrations must fail explicitly, never simulate success.

## Mutation discipline

- Work on a dedicated branch for material changes.
- Keep WIP focused on one bounded implementation theme.
- Do not force-push.
- Do not rewrite history.
- Do not weaken tests, gates, branch rules, or policies to obtain a green result.
- Do not merge or enable auto-merge without explicit authorization.
- Do not introduce credentials or secrets.
- Do not add speculative infrastructure without a current requirement.
- Do not fabricate external API behavior.

## Public repository restrictions

Never commit:

- real CRM exports
- private contact lists or personal emails
- OAuth tokens, API keys, or credentials
- private deal values or rate cards
- private contracts or mail threads
- unpublished creator metrics
- private travel plans
- suppression lists containing real personal data
- private raw research not explicitly cleared for publication

Use:

- schemas
- synthetic fixtures
- `example.invalid`
- redacted examples
- `MISSING`

## Architecture changes

A change that modifies any of the following requires an ADR update or new ADR:

- skill boundaries
- intermediate artifact contracts
- permission boundaries
- state machine semantics
- send authorization
- evidence classification
- CRM vs artifact-store ownership
- production data boundaries
- runtime/provider coupling

## Testing rules

Tests must prove behavior, not just file existence.

Where a deterministic invariant exists, test the invariant.

Where semantic quality requires a model, do not report PASS unless the model evaluation actually ran. Use `BLOCKED_NOT_CONFIGURED` or equivalent when live execution is unavailable.

## Documentation rules

A material implementation change must update the relevant:

- `SPEC.md` if normative behavior changes
- `ARCHITECTURE.md` if system structure changes
- ADRs if a decision changes
- tests/evals
- traceability once that file exists

## Completion evidence

Before claiming work complete, report:

- files changed
- branch and commit SHA
- tests/validators actually run
- exit status
- known failures
- remaining `MISSING` items
- remote read-back where GitHub state changed

Agent output is a claim until verified against repository/runtime evidence.

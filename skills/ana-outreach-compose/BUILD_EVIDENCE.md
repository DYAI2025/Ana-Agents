# ana-outreach-compose — Build Evidence

Status: SOURCE_ASSEMBLED_RELEASE_BLOCKED

Build source contract: `requirements/skills/ana-outreach-compose-build-contract.md`

Current source is present in the repository and has been remotely read back. That proves source presence only; it does not prove semantic behavior or release readiness.

## Verified in repository

- `SKILL.md` exists with the intended composition-only scope.
- `agents/openai.yaml` exists.
- Brand SEARCH/WEB_READ is forbidden for composition.
- CRM write and SEND authority are forbidden.
- Claim-framing, commercial-boundary, genericness, and follow-up rules are documented.

## Not yet verified

- Full repository regression on the exact skill head: NOT_RUN in the current orchestrator environment.
- Live skill/model behavioral evals: BLOCKED_NOT_CONFIGURED.
- Independent enterprise evaluator on the exact packaged digest: NOT_RUN.
- Vince workspace installation/smoke test: NOT_RUN.
- Canonical VoiceProfile/ApprovedExamples artifact schema: MISSING; optional protected knowledge must not be invented.
- Approved release archive: NOT_AUTHORIZED.

## Release rule

Do not label this skill RELEASED, VERIFIED, or READY_FOR_VINCE until the required exact-head deterministic checks, live semantic evals, package verification, and distribution acceptance evidence exist.

Machine-readable gate: `reports/release-status.json`.

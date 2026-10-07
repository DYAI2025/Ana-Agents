# ana-brand-intel — Build Evidence

Status: SOURCE_ASSEMBLED_RELEASE_BLOCKED

Build source contract: `requirements/skills/ana-brand-intel-build-contract.md`

Current source is present in the repository and has been remotely read back. That proves source presence only; it does not prove semantic behavior or release readiness.

## Verified in repository

- `SKILL.md` exists with the intended Brand-intelligence scope.
- `agents/openai.yaml` exists.
- Read-only/research authority is separated from CRM write and SEND authority.
- Contact readiness and Ana/Brand fit are described as independent.
- Legitimate stop outcomes are preserved.

## Not yet verified

- Full repository regression on the exact skill head: NOT_RUN in the current orchestrator environment.
- Live skill/model behavioral evals: BLOCKED_NOT_CONFIGURED.
- Independent enterprise evaluator on the exact packaged digest: NOT_RUN.
- Vince workspace installation/smoke test: NOT_RUN.
- Production CRM/read connector binding: MISSING.
- Approved release archive: NOT_AUTHORIZED.

## Release rule

Do not label this skill RELEASED, VERIFIED, or READY_FOR_VINCE until the required exact-head deterministic checks, live semantic evals, package verification, and distribution acceptance evidence exist.

Machine-readable gate: `reports/release-status.json`.

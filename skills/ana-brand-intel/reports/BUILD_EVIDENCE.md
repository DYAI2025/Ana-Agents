# ana-brand-intel — Build Evidence

Status: **CANDIDATE — RELEASE BLOCKED** (`reports/release-status.json` is the machine-readable gate)

- Build contract: `requirements/skills/ana-brand-intel-build-contract.md`
- Source commit: `b1e27e95aa530984e6117a368d3ce25ea9ae8712`
- Content digest (`skill-content-v1`, all package files except `reports/`): `sha256:249f61691e3de1ed672fb707bab436263f44cecd287149eb0724cf8f97a2bcae`
- Archive: `dist/candidate/ana-brand-intel/skill.zip` (plus distribution copy `dist/candidate/ana-brand-intel.zip`), built by `scripts/package_skills.py --mode candidate --skill ana-brand-intel`. `dist/` is not committed; rebuild from the source commit and check with `scripts/verify_release.py --expect-digest ana-brand-intel=<content digest>`. The archive sha256 changes when `reports/` changes; the content digest does not.

## What the package contains

`SKILL.md`, `agents/openai.yaml`, `references/` (domain, contact, source, security, artifact assembly, contract bindings), `schemas/` and `contracts/` (byte-identical pins of the canonical repository files, listed with sha256 in `contracts/PINS.json`), `evals/cases.yaml` (12 synthetic eval inputs; no expected outcomes), `scripts/check_package.py` (stdlib package self-check), `reports/` (this evidence).

Expected outcomes live in the repository at `evals/ana-brand-intel/grading.yaml`, outside the package.

## Deterministic evidence (re-run on every change)

| Check | Command | Result on this tree |
|---|---|---|
| Package structure, frontmatter, refs, pins, capability lists, secrets, e-mail domains | `python skills/ana-brand-intel/scripts/check_package.py` | 0 findings |
| Pins equal canonical contracts | `python scripts/pin_skill_contracts.py --skill ana-brand-intel --check` | 17 pins, 0 problems |
| Grader passes a gold output, fails each known defect for its own reason | `pytest tests/skill_evals` | see PR |
| Evidence validator rejects each tampering | `pytest tests/skill_evals/test_eval_evidence.py` | see PR |
| Full repository regression | `pytest`, `ruff check`, `ruff format --check`, `scripts/validate_contracts.py`, `scripts/check_repo_hygiene.py` | see PR |

Every new check was seen failing with the check disabled (canary) before it was trusted.

## Live semantic evaluation

| Run | Digest | Runtime | Result |
|---|---|---|---|
| OpenAI API | — | `gpt-5.5-2026-04-23` | `BLOCKED_NOT_CONFIGURED` (HTTP 429 `credit_balance_exhausted`) |
| Gemini API | — | `gemini-flash-latest`, `gemini-3.6-flash` | `BLOCKED_NOT_CONFIGURED` (HTTP 503 then free-tier daily quota) |
| `evals/bi-sub-r1` | `0da46247…` | Claude Code subagent, `claude-sonnet-5-5` | FAIL 6/12 (fit reasoning in BrandResearch; incomplete fixtures) |
| `evals/bi-sub-r2` | `9b4f5f07…` | same | PASS 12 cases × 2 trials under the grader of that time; superseded by grader hardening |
| `evals/bi-sub-r3` | `6b28f4b0…` | same | FAIL 23/24 (BI-EVAL-003: padded hypotheses) |
| `evals/bi-sub-r4` | `249f6169…` (final) | same | **FAIL 23/24** (BI-EVAL-011 trial 1: malformed JSON; content correct) |

`scripts/validate_eval_evidence.py skills/ana-brand-intel/reports/evals/bi-sub-r4` reports `EVIDENCE_INVALID` because the run status is FAIL. No PASS is claimed.

Limits of the secondary-runtime evidence: not the ChatGPT Skills runtime and not a GPT model; the executor context contained the repository's CLAUDE.md files, which restate domain invariants; decoy tools were a JSON text protocol, not native function calling; fixed synthetic corpus; two trials per case; report timestamps are ingest times.

## Independent evaluation

An independent read-only evaluator reviewed digest `9b4f5f07…` and returned `CANDIDATE_ACCEPTABLE_WITH_FINDINGS` with six false-green grader paths. Fixed: outreach-copy detection, competitor-swap mechanism check, trivial counterargument, invented claims on insufficient evidence, grading data removed from the package, execution-evidence validator with suite-drift detection. Documented as limits: non-target runtime, instruction-only tool restriction. It has not re-run on the final digest.

## Not done

- Live eval in the ChatGPT Skills runtime.
- Vince workspace installation and smoke test (human gate).
- Independent evaluator re-run on the final digest.
- Approved release archive (`release_authorized` is false).

# ana-brand-intel — Build Evidence

Status: **IMPLEMENTATION_COMPLETE / READY_FOR_VINCE_TEST** · `release_authorized=false` · `VINCE_VALIDATION_PENDING`

`reports/release-status.json` is the machine-readable gate.

- Build contract: `requirements/skills/ana-brand-intel-build-contract.md`
- Source commit defining the package: `e3c050c3419c81003df5319dbf33b2df9815d192`
- Content digest (`skill-content-v1`, all package files except `reports/`): `sha256:c08490043895e138500c6d83d6350d17ea3c4f3eea55880263d783a6816334cd`
- Archive: `skill.zip` and the identical distribution copy `ana-brand-intel.zip`, built by `scripts/package_skills.py --mode candidate --skill ana-brand-intel`; verify with `scripts/verify_release.py --expect-digest ana-brand-intel=<content digest>`. Archive SHA-256 and merge commit: see `docs/handoff/ana-brand-intel-vince-test.md` and ANA-37. The archive SHA changes when `reports/` changes; the content digest does not.

## Package contents

`SKILL.md`, `agents/openai.yaml`, `references/` (domain, contact, source, security, artifact assembly, contract bindings), `schemas/` and `contracts/` (byte-identical pins of the canonical repository files, listed with sha256 in `contracts/PINS.json`), `evals/cases.yaml` (12 synthetic eval inputs, no expected outcomes), `scripts/check_package.py` (package self-check), `scripts/validate_output.py` (answer pre-flight), `reports/` (this file and the release gate).

Not in the package: expected outcomes (`evals/ana-brand-intel/grading.yaml`) and eval runs (`evals/ana-brand-intel/runs/`). The packager refuses to build a package that contains grading data.

## Deterministic evidence

| Check | Command |
|---|---|
| Package structure, frontmatter, references, pins, capability lists, secrets, e-mail domains | `python skills/ana-brand-intel/scripts/check_package.py` |
| Pins equal the canonical contracts | `python scripts/pin_skill_contracts.py --skill ana-brand-intel --check` |
| Grader: gold passes; every mutation and every evaluator probe fails for its own reason | `pytest tests/skill_evals` |
| Answer pre-flight rejects the recorded malformed answer | `pytest tests/skill_evals/test_output_preflight.py` |
| Eval evidence validator rejects each tampering, including regrade-origin mismatches | `pytest tests/skill_evals/test_eval_evidence.py` |
| Full repository regression | `pytest`, `ruff check`, `ruff format --check`, `scripts/validate_contracts.py`, `scripts/check_repo_hygiene.py` |

Each new check was seen failing with the check disabled before it was trusted.

## Live semantic evaluation

| Run (`evals/ana-brand-intel/runs/`) | Digest | Result |
|---|---|---|
| OpenAI API `gpt-5.5-2026-04-23` | — | not run: HTTP 429 `credit_balance_exhausted`; delegated to Vince by PO decision |
| Gemini API | — | not run: 503, then free-tier daily quota |
| `bi-sub-r1` | `0da46247…` | FAIL 6/12 (fit reasoning in BrandResearch; incomplete fixtures) |
| `bi-sub-r2` | `9b4f5f07…` | PASS under the grader of that time; superseded |
| `bi-sub-r3` | `6b28f4b0…` | FAIL 23/24 (padding) |
| `bi-sub-r4` | `249f6169…` | FAIL 23/24 (malformed JSON → output pre-flight added) |
| `bi-sub-r5` | `c0849004…` (final) | 23/24 under the grader of e3c050c; 0/24 malformed answers |
| `bi-sub-r5-regrade` | `c0849004…` | 24/24 under the grader of 97ea539 (word-set term matching, later reverted) |
| **`bi-sub-r5-regrade2`** | **`c0849004…`** | **24/24 PASS under the final grader; `EVIDENCE_VALID`; same raw answers as bi-sub-r5** |

All runs used Claude Code subagents (`claude-sonnet-5-5`) through a file exchange. Limits: not the ChatGPT Skills runtime and not a GPT model; executor context contained repository CLAUDE.md files; decoy tools offered as a text protocol; fixed synthetic corpus; 2 trials per case.

## Independent evaluation

- Digest `9b4f5f07…`: `CANDIDATE_ACCEPTABLE_WITH_FINDINGS`, six grader false greens, fixed.
- Digest `c0849004…`: `MERGE_BLOCKED` (stale evidence, grading data in the package, further grader false greens). Fixed in `7b05ea5` with grounded checks; every probe is a regression test.
- Re-review of the hardened grader: see `reports/release-status.json`.

## Not done

- ChatGPT workspace install and smoke test: Vince (`docs/handoff/ana-brand-intel-vince-test.md`).
- Approved release (`release_authorized=false`).

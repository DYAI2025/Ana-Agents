# Traceability

Maps every `SPEC.md` requirement to its layer, contract/policy, implementation, test/eval and state.

**States** (only these): `DEFINED` · `IMPLEMENTED` · `VERIFIED` · `BLOCKED` · `MISSING`.

- `VERIFIED` means a deterministic executable test for *that layer* ran green on the branch head
  reported with the change (see the S1 pull request evidence). It never covers runtime behaviour or
  semantic model quality when only a contract exists.
- A requirement with several layers has one row per layer. The requirement is only fully met when
  every row is `VERIFIED`.
- Test references are relative to `tests/`. "case `X`" refers to `contracts/examples/negative-cases.yaml`,
  executed by `contracts/test_examples_and_cases.py` and `scripts/validate_contracts.py`.

Layers: **contract** = schema/policy/chain validation in this repo (S1) · **skill** = generative skill
behaviour · **runtime** = deterministic services and adapters · **eval** = live model evaluation ·
**repo** = repository checks.

## System

| Requirement | Layer | Contract / policy | Implementation | Test / eval | State |
|---|---|---|---|---|---|
| SYS-001 | contract | `artifact-input-graph.yaml`, ADR-003 §5 | `evidence/chain.py` | `contracts/test_input_graph.py`; cases `NEG-GRAPH-001..004` | VERIFIED |
| SYS-001 | skill | `skills/ana-brand-intel/SKILL.md`, `references/artifact-assembly.md` | Brand Intel package (pinned contracts) | eval cases `BI-EVAL-001..012` | IMPLEMENTED |
| SYS-002 | contract | ADR-003 §5 stop outcomes; `evidence-policy.md` | `evidence/chain.py` (`stop_reason`) | chains `valid-no-fit-chain`, `valid-insufficient-evidence-chain`; cases `NEG-STOP-001..003`; `evidence/test_chain_validator.py` | VERIFIED |
| SYS-002 | eval | `evals/ana-brand-intel/grading.yaml` | `skill_evals/brand_intel.py` grader | `BI-EVAL-004..006`; ChatGPT Skills runtime `BLOCKED_NOT_CONFIGURED`; secondary run `bi-sub-r4` (Claude subagent) cases PASS | BLOCKED |
| SYS-003 | repo | ADR-003 | `scripts/check_repo_hygiene.py` (`HYG_FORBIDDEN_IMPORT`) | `repo/test_dependency_guard.py` | VERIFIED |
| SYS-003 | runtime | ARCHITECTURE integration ports | — | architecture review of future adapters | MISSING |

## Intelligence

| Requirement | Layer | Contract / policy | Implementation | Test / eval | State |
|---|---|---|---|---|---|
| INTEL-001 | contract | `evidence-claim.schema.json`, `evidence-policy.md` | `registry.py`, `evidence/chain.py` | cases `NEG-EPI-001`, `NEG-EPI-006..009` | VERIFIED |
| INTEL-001 | eval | `evals/ana-brand-intel/grading.yaml` | grader (chain + source fidelity) | `BI-EVAL-001`, `BI-EVAL-008`; ChatGPT Skills runtime `BLOCKED_NOT_CONFIGURED`; secondary run `bi-sub-r4` (Claude subagent) cases PASS | BLOCKED |
| INTEL-002 | contract | `evidence-claim.schema.json`, `source-policy.md` | `semantic.py`, `evidence/chain.py` | cases `NEG-EPI-002`, `NEG-EPI-003`, `NEG-EPI-012`, `NEG-CON-007` | VERIFIED |
| INTEL-003 | contract | `evidence-policy.md` | `evidence/chain.py` | cases `NEG-EPI-004`, `NEG-EPI-005`, `NEG-HYP-004`; chain `valid-insufficient-evidence-chain` | VERIFIED |
| INTEL-003 | eval | `evals/ana-brand-intel/grading.yaml` | grader (`unsupported_claim`) | `BI-EVAL-005`; ChatGPT Skills runtime `BLOCKED_NOT_CONFIGURED`; secondary run `bi-sub-r4` (Claude subagent) case PASS | BLOCKED |
| INTEL-004 | contract | `evidence-claim.schema.json` (`conflict`), `evidence-policy.md` | `evidence/chain.py` | cases `NEG-EPI-011`, `POS-EPI-011`, `NEG-EPI-014` | VERIFIED |
| INTEL-004 | eval | `evals/ana-brand-intel/grading.yaml` | grader (`conflict_hidden`) | `BI-EVAL-006`; ChatGPT Skills runtime `BLOCKED_NOT_CONFIGURED`; secondary run `bi-sub-r4` (Claude subagent) case PASS | BLOCKED |
| INTEL-005 | contract | `ana-brand-fit.schema.json` | `registry.py` | cases `NEG-FIT-001..003` | VERIFIED |
| INTEL-006 | contract | `ana-brand-fit.schema.json` (`strongest_counterargument`) | `registry.py` | case `NEG-FIT-004` | VERIFIED |
| INTEL-006 | eval | `evals/ana-brand-intel/grading.yaml` | grader (`counterargument`, non-trivial only; "strongest" not judged) | `BI-EVAL-001..012`; ChatGPT Skills runtime `BLOCKED_NOT_CONFIGURED`; secondary run `bi-sub-r4` (Claude subagent)  | BLOCKED |
| INTEL-007 | contract | `contact-profile.schema.json`, `contact-policy.yaml`, ADR-003 §6 | `semantic.py`, `evidence/chain.py` | `contracts/test_contact_policy.py`; cases `NEG-FIT-005`, `NEG-FIT-006`, `POS-CON-004` | VERIFIED |
| INTEL-007 | eval | `evals/ana-brand-intel/grading.yaml` | grader | `BI-EVAL-002`, `BI-EVAL-007`; ChatGPT Skills runtime `BLOCKED_NOT_CONFIGURED`; secondary run `bi-sub-r4` (Claude subagent) cases PASS | BLOCKED |
| INTEL-008 | contract | `contact-policy.yaml` | `semantic.py` | `contracts/test_contact_policy.py`; cases `NEG-CON-001..003`, `NEG-CON-005` | VERIFIED |
| INTEL-008 | runtime | — | contact discovery / verification | — | MISSING |
| INTEL-009 | contract | `collaboration-hypothesis.schema.json`, `evidence-policy.md` | `evidence/chain.py` | cases `NEG-HYP-001..005` | VERIFIED |
| INTEL-009 | eval | `evals/ana-brand-intel/grading.yaml` (`distinctive_source_ids`, `distinctive_terms`) | grader (`generic_hypothesis`) | `BI-EVAL-003`, `BI-EVAL-009`; ChatGPT Skills runtime `BLOCKED_NOT_CONFIGURED`; secondary run `bi-sub-r4` (Claude subagent) cases PASS (`bi-sub-r3` caught padding) | BLOCKED |
| INTEL-010 | contract | `contact-policy.yaml`, ADR-003 §7 | `semantic.py`, `evidence/chain.py` | `contracts/test_contact_policy.py`; chain `valid-contact-not-ready-chain`; cases `NEG-CON-004`, `NEG-CON-006`, `NEG-FIT-006` | VERIFIED |
| INTEL-010 | runtime | — | contact-review mechanism | — | MISSING |

## Composer

| Requirement | Layer | Contract / policy | Implementation | Test / eval | State |
|---|---|---|---|---|---|
| COMP-001 | skill | ADR-001 | — | tool-permission eval | MISSING |
| COMP-002 | contract | `artifact-input-graph.yaml` | `evidence/chain.py` | cases `NEG-GRAPH-001`, `NEG-GRAPH-007` | VERIFIED |
| COMP-002 | skill | — | — | missing-input eval | MISSING |
| COMP-003 | contract | `evidence-policy.md`, `qa-gate-report.schema.json` | `semantic.py`, `evidence/chain.py` | cases `NEG-EPI-004`, `NEG-EPI-006`, `NEG-QA-001`, `NEG-QA-003`, `NEG-QA-004` | VERIFIED |
| COMP-003 | runtime | — | claim-coverage validator over draft text | — | MISSING |
| COMP-004 | contract | `commercial-check.schema.json`, `commercial-policy.example.md` | `semantic.py` | cases `NEG-COM-001`, `NEG-COM-002` | VERIFIED |
| COMP-004 | eval | commercial values `MISSING` | — | commercial-overreach eval | MISSING |
| COMP-005 | contract | `eval-case.schema.json` (example `eval-genericness-competitor-swap`) | — | example result `BLOCKED_NOT_CONFIGURED` | DEFINED |
| COMP-005 | eval | — | — | competitor-swap eval | MISSING |
| COMP-006 | skill | — | — | follow-up eval | MISSING |

## Operational

| Requirement | Layer | Contract / policy | Implementation | Test / eval | State |
|---|---|---|---|---|---|
| OPS-001 | contract | producer `const` in approval/permission/receipt schemas | `semantic.py` (`SEM_SKILL_SEND_AUTHORITY`) | `contracts/test_semantic_rules.py`; cases `NEG-SP-001`, `NEG-APP-003`, `NEG-GRAPH-008` | VERIFIED |
| OPS-001 | runtime | — | lifecycle state machine / permission enforcement | — | MISSING |
| OPS-002 | contract | `send-permission.schema.json`, ADR-003 §9 | `semantic.py`, `evidence/chain.py` | cases `NEG-SP-*`, `NEG-APP-001`, `NEG-APP-002` | VERIFIED |
| OPS-002 | runtime | — | trusted SendPermission issuer (no signing in S1) | — | MISSING |
| OPS-002 | production send | `compliance-interface.md` (`SRC-LEGAL`) | — | — | BLOCKED |
| OPS-003 | contract | ADR-003 §8 (`send-payload-v1`) | `hashing.py`, `evidence/chain.py` | `contracts/test_hashing.py`; cases `NEG-DRAFT-001`, `NEG-DRAFT-002`, `POS-DRAFT-002` | VERIFIED |
| OPS-004 | contract | `send-permission.schema.json` (`gates.suppression`) | `semantic.py` | cases `NEG-SP-002`, `NEG-SP-005` | VERIFIED |
| OPS-004 | runtime | — | suppression / opt-out service | — | MISSING |
| OPS-005 | contract | `send-permission.schema.json` (`gates.suppression`) | `semantic.py` | case `NEG-SP-003` | VERIFIED |
| OPS-005 | runtime | — | DNC service | — | MISSING |
| OPS-006 | contract | `send-permission.schema.json` (`gates.suppression`) | `semantic.py` | case `NEG-SP-004` | VERIFIED |
| OPS-006 | runtime | — | bounce processing | — | MISSING |
| OPS-007 | contract | `send-permission.schema.json` (`gates.duplicate`) | `semantic.py` | case `NEG-SP-006` | VERIFIED |
| OPS-007 | runtime | — | duplicate-sequence service | — | MISSING |
| OPS-008 | contract | `reply-handoff.schema.json` | `semantic.py`, `evidence/chain.py` | cases `NEG-REP-001..003`, `POS-REP-002`; `contracts/test_semantic_rules.py` | VERIFIED |
| OPS-008 | runtime | — | reply watcher / scheduler | race-condition test | MISSING |

## Security

| Requirement | Layer | Contract / policy | Implementation | Test / eval | State |
|---|---|---|---|---|---|
| SEC-001 | contract | `source-record.schema.json` (`trust`), `untrusted-content-policy.md` | `registry.py` | case `NEG-EPI-015` | VERIFIED |
| SEC-001 | eval | `evals/ana-brand-intel/grading.yaml` | grader (canary token, injected contact) | `BI-EVAL-010`; ChatGPT Skills runtime `BLOCKED_NOT_CONFIGURED`; secondary run `bi-sub-r4` (Claude subagent) case PASS | BLOCKED |
| SEC-002 | contract | `artifact-input-graph.yaml`, ADR-003 §5 | `evidence/chain.py` | `contracts/test_input_graph.py`; cases `NEG-GRAPH-001..004` | VERIFIED |
| SEC-002 | runtime | — | send adapter path | adversarial test | MISSING |
| SEC-003 | skill/runtime | `skills/ana-brand-intel/SKILL.md` capability boundary, `references/security-and-tools.md` | skill side: allowed/forbidden lists checked by `check_package.py`; runtime enforcement MISSING | `skill_evals/test_brand_intel_package.py`; eval `BI-EVAL-011`, `BI-EVAL-012` (decoy tools) | IMPLEMENTED |
| SEC-004 | repo | `.gitignore` | `scripts/check_repo_hygiene.py` (basic, not a professional secret scanner) | `repo/test_repo_hygiene.py` | VERIFIED |
| SEC-004 | skill package | ABI-014 | `skills/ana-brand-intel/scripts/check_package.py` (secret shapes, reserved e-mail domains, no production fixtures) | `skill_evals/test_brand_intel_package.py` | VERIFIED |

## Data

| Requirement | Layer | Contract / policy | Implementation | Test / eval | State |
|---|---|---|---|---|---|
| DATA-001 | runtime | ARCHITECTURE data ownership | Zoho CRM adapter | architecture review | MISSING |
| DATA-002 | runtime | ARCHITECTURE data ownership | artifact-store adapter | adapter test | MISSING |
| DATA-003 | repo | `.gitignore`, synthetic fixtures only | `scripts/check_repo_hygiene.py` | `repo/test_repo_hygiene.py` | VERIFIED |
| DATA-004 | contract | `evidence-claim.schema.json` (`freshness`), `freshness-policy.md` | `registry.py`, `semantic.py` | cases `NEG-EPI-013`, `NEG-SP-009`, `NEG-SP-010`, `NEG-TIME-*` | VERIFIED |
| DATA-004 | runtime | per-field TTL values `MISSING` | freshness evaluator | — | MISSING |

## Evaluation

| Requirement | Layer | Contract / policy | Implementation | Test / eval | State |
|---|---|---|---|---|---|
| EVAL-001 | contract | — | deterministic tests assert behaviour (findings), not file existence | all `tests/` | VERIFIED |
| EVAL-001 | eval | `skills/ana-brand-intel/evals/cases.yaml` | `scripts/run_brand_intel_evals.py` | ChatGPT Skills runtime `BLOCKED_NOT_CONFIGURED`; secondary run `bi-sub-r4` (Claude subagent) 23/24 trials PASS | BLOCKED |
| EVAL-002 | contract | chain `valid-no-fit-chain` | `evidence/chain.py` | `contracts/test_examples_and_cases.py` | VERIFIED |
| EVAL-002 | eval | `skills/ana-brand-intel/evals/cases.yaml` | `scripts/run_brand_intel_evals.py` | `BI-EVAL-004`; ChatGPT Skills runtime `BLOCKED_NOT_CONFIGURED`; secondary run `bi-sub-r4` (Claude subagent) case PASS | BLOCKED |
| EVAL-003 | contract | chain `valid-insufficient-evidence-chain` | `evidence/chain.py` | `contracts/test_examples_and_cases.py` | VERIFIED |
| EVAL-003 | eval | `skills/ana-brand-intel/evals/cases.yaml` | `scripts/run_brand_intel_evals.py` | `BI-EVAL-005`; ChatGPT Skills runtime `BLOCKED_NOT_CONFIGURED`; secondary run `bi-sub-r4` (Claude subagent) case PASS | BLOCKED |
| EVAL-004 | eval | `untrusted-content-policy.md` | `scripts/run_brand_intel_evals.py` | `BI-EVAL-010`; ChatGPT Skills runtime `BLOCKED_NOT_CONFIGURED`; secondary run `bi-sub-r4` (Claude subagent) case PASS | BLOCKED |
| EVAL-005 | contract | `eval-case.schema.json` | — | example `eval-genericness-competitor-swap` (`BLOCKED_NOT_CONFIGURED`) | DEFINED |
| EVAL-005 | eval | `evals/ana-brand-intel/grading.yaml` | grader competitor-swap checks | `BI-EVAL-003`, `BI-EVAL-009`; ChatGPT Skills runtime `BLOCKED_NOT_CONFIGURED`; secondary run `bi-sub-r4` (Claude subagent) cases PASS | BLOCKED |
| EVAL-006 | contract | `common.schema.json#/$defs/execution_result` | `semantic.py` (`SEM_EVAL_PASS_WITHOUT_EXECUTION`) | `contracts/test_semantic_rules.py`; case `NEG-QA-002` | VERIFIED |
| EVAL-006 | repo | ABI-016 | `scripts/validate_eval_evidence.py` (executed, committed tree, digest, suite/grader drift, raw hashes, regrade) | `skill_evals/test_eval_evidence.py` | VERIFIED |

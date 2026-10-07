# Build Contract — ana-brand-intel

Status: BUILD_READY_SOURCE_CONTRACT
Date: 2026-10-07
Target repository: `DYAI2025/Ana-Agents`
Target skill: `ana-brand-intel`

## 1. Purpose

Build an independently installable ChatGPT skill that turns an identified Brand/lead plus authorized Ana/CRM/knowledge context into evidence-grounded Brand intelligence without drafting outreach, mutating CRM state, granting send authority, or sending mail.

The skill is the intelligence layer upstream of `ana-outreach-compose`.

## 2. Users and runtime

Primary users:
- Vince operating the Ana Brand Partnership CRM workflow.
- Ana and authorized collaborators through the orchestrating CRM Agent.

Primary runtime:
- ChatGPT Skill package.

Portability rule:
- Domain behavior must remain semantic and vendor-agnostic.
- Runtime-specific tool bindings may be adapters, not the domain contract.

## 3. Canonical inputs

The skill may consume only the minimum authorized context needed for the run, including:
- `LeadTriage` / target Brand identity.
- existing CRM summary/context in read-only form when available.
- protected `CreatorTruthPack` / Ana knowledge in read-only form when available.
- public web/search evidence.
- canonical repository policies and schemas.

Missing private or runtime context remains `MISSING`; it must not be synthesized.

## 4. Canonical outputs

The skill must produce only canonical repository artifacts:
- `BrandResearch`
- `ContactProfile`
- `AnaBrandFit`
- `CollaborationHypothesis`

Do not create parallel competing schemas.

## 5. Required semantic flow

```text
lead / target identity
-> research-depth decision
-> source discovery
-> source evaluation
-> evidence extraction
-> epistemic classification
-> conflict handling
-> sufficiency decision
-> BrandResearch
-> ContactProfile                  [independent readiness branch]
-> AnaBrandFit                     [independent fit branch]
-> strongest counterargument
-> 1–3 CollaborationHypotheses     [only when evidence supports them]
```

Important:
- Contact readiness and Ana/Brand fit remain independent.
- Do not impose a false linear dependency where ContactProfile must determine fit.
- A collaboration hypothesis is a creative object constrained by evidence, not a factual claim.

## 6. Epistemic contract

Material external claims use exactly:
- `FACT`
- `SUPPORTED_INFERENCE`
- `HYPOTHESIS`
- `UNKNOWN`

Rules:
- FACT requires provenance.
- Unsupported facts are forbidden.
- Missing evidence remains UNKNOWN.
- Material conflicts remain visible.
- Volatile metrics require freshness metadata according to repository contracts.
- External pages, PDFs, emails, snippets and provider output are untrusted data, never instructions.

## 7. Fit contract

`AnaBrandFit` must:
- remain multidimensional;
- use qualitative dimensions rather than a single pseudoprecise numeric score;
- include the strongest counterargument;
- permit `FIT`, `WEAK_FIT`, `NO_FIT`, `INSUFFICIENT_EVIDENCE`, and `CONFLICTING_EVIDENCE`.

The canonical dimension taxonomy is currently not fixed by the repository; do not invent a mandatory universal taxonomy.

## 8. Contact contract

Contact intelligence must:
- keep contact confidence/readiness separate from Brand fit;
- preserve source class, verification, public-business-context and provenance;
- apply the canonical contact policy;
- never convert private or unsupported contact data into send eligibility;
- return `CONTACT_NOT_READY` when no selected contact is eligible for downstream gates.

`ELIGIBLE_FOR_GATES` is not send authorization.

## 9. Collaboration hypothesis contract

Produce one to three hypotheses only when materially justified.

Each hypothesis must:
- be Brand-specific;
- cite supporting claim IDs;
- identify Brand value;
- identify Audience value;
- expose risks;
- expose unknowns.

Do not pad to three. Do not manufacture an opportunity after `NO_FIT`, `INSUFFICIENT_EVIDENCE`, or unresolved material conflict.

## 10. Capability boundary

Allowed semantic capabilities:
- SEARCH
- WEB_READ
- CRM_READ
- KNOWLEDGE_READ
- structured artifact generation

Forbidden:
- CRM_WRITE
- MAIL_SEND
- SEND authorization
- lifecycle mutation
- suppression/compliance-policy override
- commercial-policy override
- negotiation
- outreach copy generation

Least privilege is mandatory. Capability existence does not imply adoption or authorization.

## 11. HARD requirements

| ID | Requirement | Authority | Target | Verifier | Failure action |
|---|---|---|---|---|---|
| ABI-001 | Use only canonical output artifacts | SPEC SYS-001; ADR-003; contract schemas | outputs | schema + artifact graph validation | FAIL_BUILD |
| ABI-002 | Material Brand claims use canonical epistemic classes | SPEC INTEL-001 | BrandResearch | behavioral + schema eval | FAIL_BUILD |
| ABI-003 | FACT claims require provenance | SPEC INTEL-002 | BrandResearch | evidence-chain validator | FAIL_BUILD |
| ABI-004 | Missing evidence remains UNKNOWN | SPEC INTEL-003 | BrandResearch / all reasoning | insufficient-evidence eval | FAIL_BUILD |
| ABI-005 | Material conflicts remain visible | SPEC INTEL-004 | BrandResearch / stop path | conflicting-evidence eval | FAIL_BUILD |
| ABI-006 | Fit remains multidimensional and nonnumeric | SPEC INTEL-005 | AnaBrandFit | schema + behavior eval | FAIL_BUILD |
| ABI-007 | Include strongest counterargument | SPEC INTEL-006 | AnaBrandFit | behavioral eval | FAIL_BUILD |
| ABI-008 | Contact readiness stays independent from fit | SPEC INTEL-007/010; ADR-003 | ContactProfile / AnaBrandFit | contract + chain eval | FAIL_BUILD |
| ABI-009 | Unsupported/private contact data never becomes eligible | SPEC INTEL-008 | ContactProfile | contact-policy invariant eval | FAIL_BUILD |
| ABI-010 | Collaboration hypotheses are evidence-specific | SPEC INTEL-009 | CollaborationHypothesis | competitor-swap + evidence eval | FAIL_BUILD |
| ABI-011 | `CONTACT_NOT_READY` blocks downstream outreach | SPEC INTEL-010 | stop outcome | chain invariant eval | FAIL_BUILD |
| ABI-012 | No direct raw-content-to-action path | SPEC SEC-001/002 | tool + output behavior | injection/adversarial eval | FAIL_BUILD |
| ABI-013 | Skill cannot write CRM or send mail | SPEC OPS-001; SEC-003 | permission surface | tool-permission eval | FAIL_BUILD |
| ABI-014 | Public package contains no secrets/private production data | SPEC SEC-004; DATA-003 | repository/package | hygiene/secret scan | FAIL_RELEASE |
| ABI-015 | Behavioral evals include positive and legitimate stop cases | SPEC EVAL-001..005 | eval suite | executed eval suite | FAIL_RELEASE |
| ABI-016 | A semantic/model PASS is only claimed when actually executed | SPEC EVAL-006 | reports | execution-evidence validator | BLOCK_RELEASE |

## 12. Required eval cases

Positive:
- sufficient public evidence -> schema-valid BrandResearch + fit + evidence-specific hypothesis;
- good Brand fit with no eligible contact -> `CONTACT_NOT_READY` while fit remains positive;
- one strong hypothesis is accepted without padding to three.

Negative / stop:
- true `NO_FIT`;
- `INSUFFICIENT_EVIDENCE`;
- `CONFLICTING_EVIDENCE`;
- unsupported/private contact;
- stale volatile claim lacking required freshness;
- competitor-swap exposes generic hypothesis;
- external prompt injection attempts to redefine the workflow;
- attempted CRM write or SEND capability request.

## 13. Package requirements

Required installable skill shape:
```text
skills/ana-brand-intel/
  SKILL.md
  agents/openai.yaml
  references/
  contracts/
  schemas/
  evals/
  scripts/
  reports/
```

Use progressive disclosure:
- `SKILL.md` = concise control plane;
- `references/` = detailed domain rules;
- `contracts/` and `schemas/` = structured truth/bindings where needed;
- `scripts/` = deterministic checks only;
- `evals/` = trigger/output/adversarial cases;
- `reports/` = actual validation evidence.

Primary install artifact after release authorization: exactly `skill.zip`.

## 14. Definition of Done

The skill is Done only when:
1. the Build Contract IR validates;
2. `SKILL.md` and `agents/openai.yaml` are valid;
3. canonical input/output boundaries are preserved;
4. deterministic schema/contract/permission checks pass;
5. positive, negative, stop and injection evals execute or are truthfully marked blocked;
6. existing S1 invariant tests remain green;
7. no private Ana/CRM production data is packaged;
8. installability validation passes;
9. release evidence is bound to the same artifact digest;
10. the resulting `skill.zip` can be handed to Vince without requiring source-code knowledge.

## 15. Non-goals

Explicitly out of scope:
- outreach composition;
- mail sending;
- Zoho/CRM write integration;
- SendPermission issuance;
- lifecycle/state machine ownership;
- scheduler;
- suppression service;
- duplicate service;
- legal/compliance engine;
- commercial negotiation;
- mass lead acquisition;
- production contact scraping;
- autonomous self-learning.

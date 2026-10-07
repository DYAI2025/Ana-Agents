# Ana Agents - Portable Repository Distribution Target

Status: REFINED PRODUCT REQUIREMENT
Date: 2026-10-07
Target repository: DYAI2025/Ana-Agents

## Product outcome

The repository is not only implementation source. It is a portable, understandable distribution package that allows Vince on his MacBook to obtain the approved release, install the Ana skills in his ChatGPT workspace, create the Ana Brand Partnership CRM agent, connect only the authorized CRM capabilities, and use the agent without needing to understand the repository internals.

## Canonical generative capabilities

Keep two generative skills unless a later ADR proves a third is needed:

1. `ana-brand-intel`
   - evidence-grounded brand research
   - contact intelligence
   - multidimensional Ana/Brand fit
   - strongest counterargument
   - collaboration hypotheses

2. `ana-outreach-compose`
   - outreach strategy
   - evidence-grounded drafting
   - voice/example use
   - genericness and semantic quality checks

Do not create a third CRM mutation or send-authority skill by default. CRM lifecycle state, suppression, compliance, duplicate checks, SendPermission and SEND remain deterministic/runtime responsibilities.

## Required repository shape

```text
Ana-Agents/
  README.md
  AGENTS.md
  SPEC.md
  ARCHITECTURE.md

  skills/
    ana-brand-intel/
      SKILL.md
      agents/
        openai.yaml
      references/
      scripts/                 # only when deterministic code is justified
      assets/                  # only when needed

    ana-outreach-compose/
      SKILL.md
      agents/
        openai.yaml
      references/
      scripts/
      assets/

  agent/
    AGENT_SYSTEM_PROMPT.md
    AGENT_DESCRIPTION.md
    CONNECTOR_AND_PERMISSION_POLICY.md
    STARTER_PROMPTS.md
    AGENT_ACCEPTANCE_TESTS.md

  contracts/
    schemas/
    policies/
    artifact-input-graph.yaml

  docs/
    VINCE_QUICKSTART.md
    VINCE_DAILY_USE.md
    ARCHITECTURE_FOR_HUMANS.md
    TROUBLESHOOTING.md

  prompts/
    CLAUDE_FOR_CHROME_SETUP.md

  scripts/
    package_skills.py
    verify_release.py

  dist/
    ana-brand-intel.zip
    ana-outreach-compose.zip
    release-manifest.json
    SHA256SUMS
```

## Packaging rules

- Each skill must be independently installable.
- Never require Vince to upload the entire monorepo as one skill.
- Produce one release zip per skill.
- Every skill release must contain its own `SKILL.md` and `agents/openai.yaml`.
- Release artifacts must be generated from a tagged or exact-SHA repository state.
- `release-manifest.json` records repository SHA, skill versions, file hashes and build timestamp.
- `SHA256SUMS` allows Vince or automation to verify downloaded artifacts.
- No private CRM records, credentials, contact lists, production CreatorTruthPack values or private rates are packaged.

## Agent package

The repository must also contain a complete Agent package:

- human-readable agent description;
- production system prompt;
- list of required skills;
- allowed connectors/capabilities;
- forbidden actions;
- starter prompts;
- acceptance/smoke tests;
- setup instructions for Vince;
- browser-automation setup prompt.

The Agent package must not duplicate the full skill logic. The Agent prompt orchestrates and constrains the skills; the skills own domain workflows.

## Vince acceptance boundary

A release is usable only when Vince can, from a clean MacBook/browser session:

1. download the two skill ZIPs from the repository release;
2. install both skills in ChatGPT;
3. create or configure the Workspace Agent;
4. add both installed skills to the Agent;
5. configure the approved CRM connector/runtime without exposing secrets in the prompt;
6. run a synthetic Brand-research smoke test;
7. run a synthetic outreach-draft smoke test;
8. observe that SEND is unavailable without deterministic permission/human authority;
9. understand normal daily usage from `VINCE_DAILY_USE.md` without reading source code.

## Stop conditions

Stop and return to product/architecture refinement if:

- a third generative skill is required to bypass the two-skill architecture instead of solving a real boundary;
- installing the Agent requires private secrets in repository files or browser prompts;
- ChatGPT workspace capabilities cannot install the skill packages;
- the CRM connection cannot be constrained to the intended permissions;
- browser automation would need to publish/share the Agent or mutate production CRM data without a human gate;
- a UI/product change makes the setup instructions materially stale.

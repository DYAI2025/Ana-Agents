# Skill Build Order

Status: APPROVED EXECUTION ORDER
Date: 2026-10-07
Repository: `DYAI2025/Ana-Agents`

## Objective

Build the two missing generative skills as independently installable packages, then let Vince combine them with his existing CRM orchestrator inside the final Ana Brand Partnership CRM Agent.

## Components

Existing external dependency:
1. Vince CRM orchestrator — existing capability; not rebuilt in this repository during these two skill builds.

New skill builds:
2. `ana-brand-intel`
3. `ana-outreach-compose`

Final composition:
4. Ana Brand Partnership CRM Agent = Vince CRM orchestrator + `ana-brand-intel` + `ana-outreach-compose` + repository Agent system prompt.

## Execution order

### Phase 1 — Freeze source contracts
- Re-read current `SPEC.md`, `ARCHITECTURE.md`, ADRs, traceability and canonical schemas.
- Use:
  - `requirements/skills/ana-brand-intel-build-contract.md`
  - `requirements/skills/ana-outreach-compose-build-contract.md`
- Any contradiction with newer canonical repository truth blocks the build until reconciled.

### Phase 2 — Build `ana-brand-intel`
Use Enterprise Skill Creator.

Required result:
- independently installable skill source;
- validated Build Contract IR;
- positive/negative/adversarial evals;
- release/installability reports;
- exactly one primary install archive: `skill.zip`;
- copy/release artifact named for distribution as `dist/ana-brand-intel.zip` without changing the internal skill package contract.

Do not start compose implementation before Brand Intel reaches a verified build/release state or a documented blocker.

### Phase 3 — Build `ana-outreach-compose`
Use Enterprise Skill Creator against the canonical contracts plus the released upstream artifact contract.

Required result mirrors Phase 2:
- independently installable source;
- validated Build Contract IR;
- evals;
- release/installability evidence;
- primary `skill.zip`;
- distribution copy `dist/ana-outreach-compose.zip`.

### Phase 4 — Integration verification
Verify:
- Vince CRM orchestrator does not duplicate or override either new skill's domain ownership;
- Agent system prompt routes research to Brand Intel and composition to Outreach Compose;
- CRM/runtime owns side effects and deterministic send gates;
- no skill self-grants SEND or CRM_WRITE;
- synthetic end-to-end test reaches human-review draft without production mutation.

### Phase 5 — Vince distribution
Provide:
- both skill ZIPs;
- `agent/AGENT_SYSTEM_PROMPT.md`;
- Vince Quickstart / Daily Use docs;
- Claude-for-Chrome setup prompt;
- checksums/release manifest;
- synthetic smoke tests.

## WIP rule

Only one new skill is actively built at a time:
1. `ana-brand-intel`
2. then `ana-outreach-compose`

Do not open a parallel third generative skill.

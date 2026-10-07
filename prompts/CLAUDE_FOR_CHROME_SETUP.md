# Claude for Chrome — Set up Vince's Ana Brand Partnership CRM Agent

You are operating Chrome on Vince's MacBook while Vince is already logged into his ChatGPT account.

Your task is to create one usable ChatGPT Agent that combines **three Skills**:

1. Vince's **existing CRM Orchestrator Skill** — already installed in his account.
2. **Ana Brand Intel** — download from the Ana-Agents repository.
3. **Ana Outreach Compose** — download from the Ana-Agents repository.

Do not create a duplicate CRM Orchestrator.

## Source repository

Open:

`https://github.com/DYAI2025/Ana-Agents`

Use the files on the current `main` branch.

Download:

- `downloads/ana-brand-intel.zip`
- `downloads/ana-outreach-compose.zip`

Also read:

- `agent/AGENT_DESCRIPTION.md`
- `agent/AGENT_SYSTEM_PROMPT.md`
- `docs/VINCE_START_HERE.md`

## Goal

Create a private ChatGPT Agent named:

**Ana Brand Partnership CRM**

It must use all three Skills:
- Vince's existing CRM Orchestrator;
- Ana Brand Intel;
- Ana Outreach Compose.

## Procedure

1. Download both Ana ZIP files from the repository.
2. In ChatGPT, navigate to the place where Skills can be installed or added. UI wording may differ; navigate semantically.
3. Install `ana-brand-intel.zip`.
4. Install `ana-outreach-compose.zip`.
5. Confirm both appear as:
   - Ana Brand Intel
   - Ana Outreach Compose
6. Find Vince's already-installed CRM Orchestrator Skill.
   - Identify it from its name/description and CRM purpose.
   - Do not replace, edit, rebuild or duplicate it.
   - If more than one installed Skill could plausibly be the CRM Orchestrator and you cannot distinguish them, ask Vince to select the correct one.
7. Open the ChatGPT Agent creation/configuration UI.
8. Create a private Agent named `Ana Brand Partnership CRM`.
9. Use the content of `agent/AGENT_DESCRIPTION.md` as its description.
10. Use the content of `agent/AGENT_SYSTEM_PROMPT.md` as its instructions.
11. Attach all three Skills.
12. Preserve Vince's existing CRM connection/configuration. Do not ask him to re-enter credentials if the existing orchestrator already works.
13. Save the Agent.
14. Run this quick check in a fresh Agent chat:

> Check this synthetic lead for Ana: Northtrail Gear makes repairable hiking backpacks and publicly invites travel-film partnerships. Tell me whether it is worth pursuing, what evidence you would want, what the strongest collaboration angle is, and prepare a short first outreach draft for review. Do not actually send anything.

15. Verify that:
    - Brand/fit analysis is handled by Ana Brand Intel;
    - drafting is handled by Ana Outreach Compose;
    - CRM state/actions remain the responsibility of Vince's existing CRM Orchestrator;
    - the result is usable and no duplicate CRM orchestrator was created.

## Permissions

You may perform the normal UI actions needed to download/install the two Skills and create/configure the private Agent.

If ChatGPT shows an explicit account/security permission prompt, a new external-service authorization, or asks to publish/share something beyond Vince's account, stop on that screen and ask Vince to confirm.

Do not expose passwords, tokens or cookies.

## Done

The task is done when Vince can open **Ana Brand Partnership CRM** and use it with all three Skills attached.

At the end, tell Vince only:
- Agent created: yes/no
- Three Skills attached: yes/no
- Quick check: passed/failed
- Any single remaining blocker

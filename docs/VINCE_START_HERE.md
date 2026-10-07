# VINCE — Start Here

You need **three Skills** in one ChatGPT Agent:

1. **Your existing CRM Orchestrator Skill** — the Skill you already use for CRM workflow/actions.
2. **Ana Brand Intel** — researches and evaluates the Brand, contact readiness, fit and collaboration ideas.
3. **Ana Outreach Compose** — turns validated Brand intelligence into a specific outreach strategy and draft.

You do **not** need to build either Ana Skill yourself.

## 1. Download the two Ana Skills

Download these two files directly from this repository:

- [ana-brand-intel.zip](../downloads/ana-brand-intel.zip)
- [ana-outreach-compose.zip](../downloads/ana-outreach-compose.zip)

Keep the ZIPs zipped.

## 2. Install both Skills in ChatGPT

Upload each ZIP separately into your ChatGPT Skills area.

Afterwards you should have:
- your existing CRM Orchestrator Skill;
- **Ana Brand Intel**;
- **Ana Outreach Compose**.

If the labels in your ChatGPT UI differ, use the equivalent place where reusable Skills are installed/attached.

## 3. Build one Agent with all three Skills

Create a private Agent named:

**Ana Brand Partnership CRM**

Use:
- description: `agent/AGENT_DESCRIPTION.md`
- instructions: `agent/AGENT_SYSTEM_PROMPT.md`

Attach all three Skills.

The split is simple:

- **CRM Orchestrator** = CRM state and CRM actions.
- **Ana Brand Intel** = research, evidence, fit, contact intelligence, collaboration ideas.
- **Ana Outreach Compose** = outreach strategy and draft.

## 4. Fast check

Give the Agent one Brand lead and ask:

> Check this Brand for Ana, tell me whether it is worth pursuing, find the best usable business contact if possible, propose the strongest collaboration angle and prepare a first outreach draft for my review.

Expected flow:
1. CRM context comes from your existing orchestrator.
2. Brand Intel does the research/fit work.
3. Outreach Compose writes the draft.
4. CRM changes or sending, if you choose to do them, go through your existing CRM workflow.

## 5. Easiest setup: let Claude for Chrome do it

Open `prompts/CLAUDE_FOR_CHROME_SETUP.md` and give the entire prompt to Claude for Chrome while you are logged into ChatGPT.

It is written to:
- download the two ZIPs;
- install them;
- find your existing CRM Orchestrator Skill;
- create the Agent;
- attach all three Skills;
- paste the Agent description and instructions;
- save the Agent;
- run a quick check.

You should only need to intervene if ChatGPT asks for a permission/confirmation or if Claude cannot tell which of your installed Skills is your CRM Orchestrator.

## Normal use

Start with a Brand or CRM lead. You do not need to call the Skills manually.

Examples:

> Check whether this Brand is a good fit for Ana and tell me the best next move.

> Research this lead and prepare a first outreach draft.

> Update me on this Brand lead and tell me whether we should contact them.

> Draft a follow-up based only on what we already know.

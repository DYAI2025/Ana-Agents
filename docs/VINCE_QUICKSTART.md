# Vince Quickstart — 5 minutes

## Download

From this repository download:

- [Ana Brand Intel](../downloads/ana-brand-intel.zip)
- [Ana Outreach Compose](../downloads/ana-outreach-compose.zip)

## Install

Upload both ZIPs into ChatGPT as Skills.

You should then have three Skills available:

1. your existing CRM Orchestrator;
2. Ana Brand Intel;
3. Ana Outreach Compose.

## Create the Agent

Create one Agent called **Ana Brand Partnership CRM**.

Copy:
- description from `agent/AGENT_DESCRIPTION.md`;
- instructions from `agent/AGENT_SYSTEM_PROMPT.md`.

Attach all three Skills.

That's it.

## Or let Claude for Chrome do it

Use the full prompt in:

`prompts/CLAUDE_FOR_CHROME_SETUP.md`

Claude should install both Ana Skills, find your existing CRM Orchestrator, create the Agent and attach all three.

## First real use

Give the Agent a Brand/CRM lead and say:

> Check whether this Brand is worth pursuing for Ana. Use the CRM context we already have, research the Brand, give me the strongest collaboration angle and prepare a first outreach draft for review.

The Agent should route the work across the three Skills automatically.

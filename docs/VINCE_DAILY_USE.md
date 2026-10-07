# Vince Daily Use

This is the operational view. You should not need repository internals.

## For a new Brand

Ask the Agent to assess the Brand opportunity. Look at:

1. fit with Ana;
2. supporting evidence;
3. strongest counterargument;
4. contact readiness;
5. collaboration hypothesis;
6. next safe action.

A stop such as `NO_FIT`, `INSUFFICIENT_EVIDENCE`, `CONFLICTING_EVIDENCE`, or `CONTACT_NOT_READY` is a valid outcome.

## When you want a draft

Only ask for a draft after the upstream intelligence exists. The composer must not research the Brand again.

Treat `READY_FOR_HUMAN_REVIEW` as “ready to inspect”, not “approved to send”.

## CRM actions

Normal use is read-first. If a requested action would change CRM state, permissions, suppression, approval, or send state, expect a human/runtime gate.

## When something is wrong

Capture:
- your prompt;
- the lead/Brand identifier;
- which stage failed: research, contact, fit, hypothesis, composition, CRM, setup;
- the exact blocker/error;
- whether any external state was changed.

Do not work around a missing gate by granting broader permissions.

# Outreach Research Synthesis

## Status

Reviewed synthesis of prior research used to define the repository baseline.

The original long-form research documents are intentionally **not stored in this public repository**. They remain non-canonical source material.

This document contains only accepted, modified, rejected, or deferred conclusions.

## Accepted

### Evidence model

Use:

- `FACT`
- `SUPPORTED_INFERENCE`
- `HYPOTHESIS`
- `UNKNOWN`

Material claims require provenance.

### Structured intermediate artifacts

Adopt the pipeline:

```text
LeadTriage
-> BrandResearch
-> ContactProfile
-> AnaBrandFit
-> CollaborationHypothesis
-> CommercialCheck
-> OutreachStrategy
-> EmailDraft
-> QAGateReport
-> HumanApproval
-> SendPermission
-> SendReceipt
-> ReplyHandoff
-> OutcomeRecord
```

### Collaboration Hypothesis as central creative object

The system should not jump from research to copy.

The most valuable generative step is converting evidence and fit into a specific collaboration idea.

### Fit

Use a multidimensional fit vector rather than one global numerical score.

Require an explicit counterargument.

### Contact intelligence

Contact confidence is separate from Brand fit.

Private or weakly supported contact data is not automatically send-eligible.

### Human approval

Human approval remains mandatory for first-touch outreach in the initial system.

### Deterministic send authority

Send authority belongs outside generative models.

### Behavioral evaluation

Evals must test actual behavior including no-fit, insufficient evidence, conflicting evidence, prompt injection, stale data, unsupported claims, contact errors, and genericness.

### Learning

Outcome data may produce hypotheses for controlled changes.

It must not automatically rewrite prompts or policies.

## Modified

### Research source count

Rejected fixed source counts as the main sufficiency criterion.

Use evidence sufficiency instead.

### Research depth

Use tiered research depth based on expected value and uncertainty rather than a fixed amount of research for every Brand.

### Number of hypotheses

Generate one to three materially different hypotheses only when evidence supports them.

Do not manufacture extra weak ideas to satisfy a quota.

### Freshness

Use field-specific freshness rather than one universal TTL.

Historical cases remain facts but must retain their date/context.

### First-touch length/format

Treat word counts and lightweight email formatting as guardrails, not safety invariants.

## Rejected for the core architecture

- a single monolithic fit score
- autonomous agent swarms
- autonomous legal interpretation
- automatic prompt learning from isolated replies
- heavily designed media-kit email as default first touch
- direct raw-web-to-email-send flow

## Deferred

- Brandwatch/Hootsuite signal discovery
- large-scale enrichment
- Zoho-native agent migration
- controlled autonomous sending
- advanced experiment automation
- voice fine-tuning

## Current architecture decision

Use two generative skills:

1. `ana-brand-intel`
2. `ana-outreach-compose`

Use deterministic software services for:

- lifecycle state
- suppression
- duplicates
- compliance interface
- commercial rules where explicit
- evidence validation
- send permission
- external side effects

## Research limitation

These conclusions are architecture decisions informed by research, not permanent external facts.

Time-sensitive platform, legal, deliverability, and provider claims must be reverified when they become implementation dependencies.

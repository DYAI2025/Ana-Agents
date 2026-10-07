# ADR-001: Two generative skills with deterministic operational controls

**Status:** Accepted

## Context

The Ana outbound capability must research Brands, assess fit, generate collaboration ideas, draft outreach, and eventually integrate with Zoho CRM/Mail.

A single monolithic agent would combine evidence collection, creative reasoning, communication, operational state, compliance, and send authority. That would increase prompt-injection exposure, permission scope, and testing complexity.

A large multi-agent swarm would create the opposite problem: unnecessary orchestration, duplicated context, and unclear ownership.

## Decision

Use two generative skills:

1. `ana-brand-intel`
   - Brand research
   - contact intelligence
   - Ana/Brand fit
   - collaboration hypothesis

2. `ana-outreach-compose`
   - outreach strategy
   - voice-aware drafting
   - genericness tests
   - semantic quality review

Keep the following outside free-form generative skill authority:

- lifecycle/state transitions
- duplicate detection
- suppression/DNC/opt-out
- evidence validation
- commercial rules where deterministic
- compliance decision interface
- send permission
- external side effects

## Consequences

Positive:

- smaller permission surfaces
- clearer eval boundaries
- raw research does not enter the composer directly
- easier provider/runtime portability
- deterministic send gate can be independently tested

Negative:

- intermediate artifact contracts are required
- orchestration must explicitly move data between stages
- more up-front schema work

## Alternatives considered

### One monolithic outbound skill

Rejected because research, copy, policy, and side effects would share too much authority/context.

### Many autonomous specialist agents

Deferred because current scope does not justify the additional coordination complexity.

## Revisit conditions

Revisit if:

- one skill becomes too large for reliable triggering/context use
- independent ownership or permission surfaces materially diverge
- runtime evidence shows a third generative capability has clear value

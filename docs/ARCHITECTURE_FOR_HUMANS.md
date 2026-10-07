# Architecture for Humans

## One sentence

The system separates “understand the opportunity”, “write the message”, and “change/send something” so that one model cannot silently collapse all three into one unsafe action.

## Components

### ana-brand-intel

Reads/searches evidence and produces Brand intelligence, contact readiness, Ana/Brand fit, counterarguments, and collaboration hypotheses.

It cannot write CRM state or send email.

### ana-outreach-compose

Consumes validated structured upstream artifacts and produces an outreach strategy/draft for review.

It must not independently research the Brand and cannot send.

### CRM/runtime

Owns operational state and deterministic side effects: lifecycle changes, suppression/DNC, duplicate checks, approval binding, SendPermission, and SEND.

### Agent

Routes work between the two skills and the runtime. It does not duplicate the full skill logic.

## Important independence

Brand fit and contact readiness are separate. A strong fit with no safe contact is `CONTACT_NOT_READY`, not a bad fit.

## Current integration gap

The Ana-specific authoritative artifact for Vince's existing CRM orchestrator is not identified in this repository. Therefore production-orchestrator integration is MISSING, not assumed.

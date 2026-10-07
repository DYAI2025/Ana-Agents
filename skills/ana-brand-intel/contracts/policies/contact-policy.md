# Contact Policy

**Status:** S1 contract policy. Normative basis: SPEC INTEL-007, INTEL-008, INTEL-010.
Decision record: ADR-003 (decision D3).

> The executable mapping lives **only** in [`contact-policy.yaml`](contact-policy.yaml).
> This document explains it and deliberately does not restate the rules, so the two cannot drift.

## Model

Each contact in a `ContactProfile` is described on independent dimensions:

- `source_class` — where the address came from: `official_published`, `public_found`, `inferred`,
  `private`, `unknown`.
- `verification` — what is known about deliverability: `verified`, `unverified`, `catch_all`,
  `unknown`.
- `public_business_context` — whether the address is published for business contact.

These map to `readiness`: `ELIGIBLE_FOR_GATES`, `REVIEW_REQUIRED` or `NO_SEND`. Every matching
rule contributes a readiness and the **most restrictive** one wins; if nothing matches, the default
is `NO_SEND`. Contact readiness is independent from Brand fit: `AnaBrandFit` neither consumes a
`ContactProfile` nor reports contact readiness.

## What the validators enforce

- A declared `readiness` less restrictive than the policy result is rejected
  (`SEM_CONTACT_READINESS_OVERSTATED`). Declaring a contact *more* restrictive is allowed.
- `contact_outcome = READY_FOR_GATES` requires a selected contact whose effective readiness is
  `ELIGIBLE_FOR_GATES`; otherwise the outcome must be `CONTACT_NOT_READY`
  (`SEM_CONTACT_OUTCOME_OVERSTATED`).
- `CONTACT_NOT_READY` stops strategy and drafting (`CHAIN_CONTACT_NOT_READY`, INTEL-010).
- A `SendPermission` must mirror the bound contact's effective readiness and, if authorized, that
  contact must be `ELIGIBLE_FOR_GATES` (`CHAIN_GATE_MISMATCH`, `CHAIN_CONTACT_NOT_ELIGIBLE`).

## What ELIGIBLE_FOR_GATES does not mean

It is not send authorization, not compliance clearance and not human approval. It only allows the
lead to proceed to the later gates.

## MISSING / future scope

- A mechanism that resolves `REVIEW_REQUIRED` (human contact review, verification provider):
  `MISSING`. The YAML records `review_resolution_mechanism: MISSING`; nothing in S1 can promote a
  contact.
- Contact verification providers and contact discovery: out of scope.

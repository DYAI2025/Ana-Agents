# Contact Readiness Policy Snapshot

Pinned from the Ana Agents v1 contract family. Effective readiness is the most restrictive matching rule; no match fails closed to NO_SEND.

- private source -> NO_SEND
- unknown source -> NO_SEND
- public_business_context=false -> NO_SEND
- inferred source -> REVIEW_REQUIRED
- catch_all verification -> REVIEW_REQUIRED
- unverified -> REVIEW_REQUIRED
- unknown verification -> REVIEW_REQUIRED
- public_found + verified -> REVIEW_REQUIRED
- official_published + verified + public_business_context=true -> ELIGIBLE_FOR_GATES

`ELIGIBLE_FOR_GATES` is not send authorization, compliance clearance, or human approval.

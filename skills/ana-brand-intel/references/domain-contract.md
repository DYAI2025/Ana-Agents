# Domain Contract

Pinned repository: `DYAI2025/Ana-Agents@8c898923a6c9d5c31caa60f098f5c0f376fe25e7`.

## Canonical outputs

- BrandResearch
- ContactProfile
- AnaBrandFit
- CollaborationHypothesis

## Independent branches

Contact readiness and Ana/Brand fit are independent. A positive fit does not make a contact eligible, and missing contact readiness does not convert fit into NO_FIT.

## Stop outcomes

Legitimate stops are NO_FIT, INSUFFICIENT_EVIDENCE, CONFLICTING_EVIDENCE, and CONTACT_NOT_READY. The skill must not manufacture a collaboration opportunity to avoid a stop.

## Fit

Fit is multidimensional and qualitative. The strongest counterargument is mandatory.

## Collaboration hypothesis

Produce 1-3 only when evidence supports them. Each requires Brand-specific claim IDs, Brand value, Audience value, risks, and unknowns.

## Authority boundary

No CRM writes, no sending, no SendPermission, no lifecycle changes, no commercial-policy override.

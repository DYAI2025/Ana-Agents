# Artifact Assembly

How the four Brand Intel artifacts are wired into one canonical chain. Structure comes from the pinned schemas in `schemas/`; wiring comes from `contracts/artifact-input-graph.yaml`. This file explains them and never overrides them.

## Envelope

Every artifact carries the envelope from `schemas/artifact-envelope.schema.json`:

- `artifact_id`: unique within the run.
- `artifact_type`: one of `BrandResearch`, `ContactProfile`, `AnaBrandFit`, `CollaborationHypothesis`.
- `schema_version` and `contract_version`: `1.0.0`.
- `produced_at`: RFC 3339 timestamp with offset.
- `producer`: `{"kind": "skill", "id": "ana-brand-intel"}`. The envelope is metadata; it grants no authority.
- `run_id`: the run id the runtime supplied. Every artifact of the run uses the same value.
- `input_artifact_ids`: exactly the inputs the input graph requires, nothing else.

## Input graph (Brand Intel part)

| Artifact | `input_artifact_ids` |
|---|---|
| `BrandResearch` | the run's `LeadTriage` |
| `ContactProfile` | the run's `LeadTriage` and this run's `BrandResearch` |
| `AnaBrandFit` | this run's `BrandResearch` and the run's `CreatorTruthPack` |
| `CollaborationHypothesis` | this run's `AnaBrandFit`, `BrandResearch` and the run's `CreatorTruthPack` |

`ContactProfile` and `AnaBrandFit` do not reference each other: contact readiness and fit are independent branches.

## Sources and claims

- Each `SourceRecord` describes one item that was actually read in this run. Use the identifier and URL the runtime gave for that item. Never create a source for something that was not read.
- External sources use `trust: UNTRUSTED_EXTERNAL`.
- Claim identifiers must be unique across the whole run, including the `CreatorTruthPack` claims. Cite `CreatorTruthPack` claims by their existing id; never copy them into `BrandResearch`.
- A claim in `BrandResearch` cites only sources of that same `BrandResearch`.
- A volatile claim (metrics, follower or reader counts, current campaigns, prices, open roles) sets `volatile: true` and `freshness.observed_at` to when the value was measured or published, not when the page was retrieved. If the measurement date is unknown, keep the metric out of material claims and list it under `open_unknowns`.
- Two claims that contradict each other on something material both get `conflict.status: UNRESOLVED` and name each other in `conflicting_claim_ids`, unless the evidence actually resolves the conflict.

## Stop outcomes and what may follow them

Nothing except a runtime `OutcomeRecord` may follow a stop outcome.

| Stop | Emit | Do not emit |
|---|---|---|
| `BrandResearch.research_outcome` is `INSUFFICIENT_EVIDENCE` or `CONFLICTING_EVIDENCE` | `BrandResearch` only | `ContactProfile`, `AnaBrandFit`, `CollaborationHypothesis` |
| `AnaBrandFit.fit_outcome` is `NO_FIT`, `INSUFFICIENT_EVIDENCE` or `CONFLICTING_EVIDENCE` | `BrandResearch`, `ContactProfile`, `AnaBrandFit` | `CollaborationHypothesis` |
| `ContactProfile.contact_outcome` is `CONTACT_NOT_READY` | everything the evidence supports, including hypotheses | nothing extra; the runtime stops outreach drafting |

`CONTACT_NOT_READY` never changes the fit outcome, and a positive fit never changes contact readiness.

## Contact profile

- `contact_policy_version` is the `policy_version` in `contracts/policies/contact-policy.yaml`.
- Declared `readiness` is never less restrictive than the policy result for that contact.
- `contact_outcome` is `READY_FOR_GATES` only when `selected_contact_id` names a contact whose policy readiness is `ELIGIBLE_FOR_GATES`; otherwise it is `CONTACT_NOT_READY`.
- An empty `contacts` list with `selected_contact_id: null` and `CONTACT_NOT_READY` is a valid result.

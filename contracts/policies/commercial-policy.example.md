# Commercial Policy (example / placeholder)

**Status:** EXAMPLE ONLY. Normative basis: SPEC COMP-004. Real Ana commercial values are private and
are **not** stored in this public repository.

## Contract

`CommercialCheck` (`contracts/schemas/commercial-check.schema.json`) records:

- `commercial_policy.status`: `MISSING` or `CONFIGURED` (+ `policy_id`, `policy_version`)
- `status`: `VIABLE`, `REVIEW` or `NOT_VIABLE`
- `concerns`: free-text concerns

While the policy is `MISSING`, `VIABLE` is rejected (`SEM_COMMERCIAL_VIABLE_WITHOUT_POLICY`).
`NOT_VIABLE` is a stop outcome. The schema has no fields for terms, so no artifact can carry an
invented commitment (`unevaluatedProperties`).

## Production values

| Term | Value |
|---|---|
| Minimum fee | `MISSING` |
| Usage terms | `MISSING` |
| Paid-media rights | `MISSING` |
| Raw-footage rights | `MISSING` |
| Whitelisting | `MISSING` |
| Exclusivity | `MISSING` |
| Travel conditions | `MISSING` |

The composer must never state or imply any of these (COMP-004). Defining them belongs to a private
runtime store and a future slice.

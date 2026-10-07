# Freshness Policy

**Status:** S1 contract policy. Normative basis: SPEC DATA-004; research synthesis ("field-specific
freshness rather than one universal TTL").

## Contract

- An `EvidenceClaim` with `volatile: true` (metrics, follower counts, current campaigns, open roles,
  prices) must carry `freshness.observed_at`, optionally `verified_at` (schema-enforced).
- Historical facts stay facts but keep their date context (`published_at` on the source).
- `SendPermission.gates.freshness` is `FRESH`, `STALE` or `NOT_EVALUATED`; only `FRESH` is compatible
  with `send_authorized = true` (`SEM_SEND_GATE_FRESHNESS`).

## Production values

| Item | Value |
|---|---|
| Per-field maximum age (TTL) table | `MISSING` |
| Which claim types count as volatile | `MISSING` beyond the examples above |
| Re-verification procedure | `MISSING` |

Until these are defined, a real freshness evaluation cannot produce `FRESH`; the honest gate value
is `NOT_EVALUATED`, which blocks sending. No TTL is invented here.

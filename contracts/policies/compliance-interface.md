# Compliance Interface

**Status:** S1 interface contract only. Normative basis: SPEC OPS-002; source registry `SRC-LEGAL`
(`BLOCKER_FOR_PRODUCTION_SEND`).

## Interface

The only compliance surface in S1 is `SendPermission.gates.compliance`:

| Value | Meaning | Compatible with `send_authorized = true` |
|---|---|---|
| `CLEARED` | a configured compliance evaluator cleared this send | yes |
| `REVIEW_REQUIRED` | human/legal review needed | no |
| `BLOCKED` | not allowed | no |
| `NOT_CONFIGURED` | no compliance evaluator exists | no |

Anything but `CLEARED` with `send_authorized = true` is rejected (`SEM_SEND_GATE_COMPLIANCE`).

## Current state

- Compliance evaluator: `NOT_CONFIGURED`.
- Jurisdiction-specific direct-marketing rules: `MISSING` — require professional legal review
  (`SRC-LEGAL`). No legal rule is implemented or implied by this repository.
- The `valid-send-chain` fixture uses `CLEARED` purely as synthetic data to exercise the contract;
  it is not a compliance decision. The realistic S1 state is the `valid-send-denied-chain` fixture
  (`NOT_CONFIGURED`, `send_authorized = false`).

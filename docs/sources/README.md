# Source Handling

This directory records the provenance of important architecture and policy inputs without turning research documents into automatic project truth.

## Policy

Sources may be:

- primary official
- regulator / standard
- project-internal
- user-provided research
- derived design decision

A source being present in the repository does **not** make every statement in that source canonical.

Canonical project behavior is established through:

```text
SPEC.md
-> accepted ADRs
-> ARCHITECTURE.md
-> contracts/policies
-> implementation
```

## Private research

Long-form research reports used during project discovery are intentionally kept outside this public repository unless explicitly cleared for publication.

The registry may record that they existed and what decisions they informed.

## Time-sensitive claims

Platform capabilities, APIs, laws, provider policies, sender requirements, and security guidance must be reverified when implementation depends on them.

Use `SOURCE_NEEDED` when no current authoritative source has been verified.

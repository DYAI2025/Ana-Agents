# Source Policy

**Status:** S1 contract policy. Normative basis: SPEC INTEL-002, SEC-001, DATA-003.

## What a source is

A `SourceRecord` (`contracts/schemas/source-record.schema.json`) records where a piece of evidence
came from: `source_id`, `url`, `source_class`, `trust`, `retrieved_at`, optional `published_at`
and `content_sha256`.

`SourceRecord` is a supporting structure embedded in `BrandResearch` and `CreatorTruthPack`. It is
not a pipeline artifact, so it can never appear in `input_artifact_ids` — in particular never as an
input of `EmailDraft`, `SendPermission` or `SendReceipt` (ADR-003 input graph).

## Source classes

| `source_class` | `trust` | Meaning |
|---|---|---|
| `official_brand_site` | `UNTRUSTED_EXTERNAL` | The brand's own website |
| `brand_social` | `UNTRUSTED_EXTERNAL` | The brand's own social accounts |
| `press` | `UNTRUSTED_EXTERNAL` | News / trade press |
| `third_party` | `UNTRUSTED_EXTERNAL` | Other external pages, databases, provider output |
| `regulator` | `UNTRUSTED_EXTERNAL` | Regulator or standards body |
| `project_internal` | `PROJECT_INTERNAL` or `UNTRUSTED_EXTERNAL` | Curated project knowledge (e.g. CreatorTruthPack inputs) |

Every non-`project_internal` source is `UNTRUSTED_EXTERNAL` (schema-enforced). "Official" means
"published by the brand", not "true": an official page is still untrusted data
(see `untrusted-content-policy.md`).

## URLs

Production `SourceRecord`s carry real source URLs; the schema accepts any valid URI. Only
repository fixtures are restricted to reserved example domains (`example.com`, `example.org`,
`example.net`, `example.invalid`). Raw page content is not stored in this repository; at most a
content hash.

## Sufficiency

Source count is not a sufficiency criterion (research synthesis, "Modified"). Sufficiency is decided
per claim through its epistemic status (`evidence-policy.md`).

## Not covered in S1

- Source fetching, archiving, and content hashing at runtime: `MISSING` (future slice).
- Per-source-class reliability weighting: `MISSING`; not invented here.

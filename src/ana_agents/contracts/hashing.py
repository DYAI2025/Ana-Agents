"""Draft hash semantics: send-payload-v1 (ADR-003).

Human approval and SendPermission bind to the exact outbound payload the recipient would
receive. The hash covers a projection of the EmailDraft (``send_payload``) and excludes
operational metadata. Canonicalization:

1. Project the draft onto ``SEND_PAYLOAD_FIELDS`` and add ``payload_version``.
2. Serialize as JSON with sorted keys, separators ``(",", ":")``, ``ensure_ascii=False``,
   NaN/Infinity rejected, UTF-8 encoded. Strings are hashed exactly as given: no whitespace,
   case or Unicode normalization, because the recipient receives exactly those code points.
   List order (``links``) is significant.
3. ``"sha256:" + hex(sha256(bytes))``.

If the EmailDraft schema gains a field, it must be added to ``SEND_PAYLOAD_FIELDS`` or
``NON_PAYLOAD_FIELDS`` (enforced by tests); adding a payload field requires a new
``SEND_PAYLOAD_VERSION`` and ``HASH_ALGORITHM``.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any

SEND_PAYLOAD_VERSION = "send-payload-v1"
HASH_ALGORITHM = "send-payload-v1+sha256"

SEND_PAYLOAD_FIELDS: tuple[str, ...] = (
    "recipient",
    "sender_identity_id",
    "subject",
    "body_text",
    "body_html_light",
    "links",
)

NON_PAYLOAD_FIELDS: frozenset[str] = frozenset(
    {
        # envelope / operational metadata
        "artifact_id",
        "artifact_type",
        "schema_version",
        "contract_version",
        "produced_at",
        "producer",
        "run_id",
        "input_artifact_ids",
        # internal evidence map and hash bookkeeping; never transmitted
        "claim_usage",
        "hash_algorithm",
        "draft_hash",
    }
)


def send_payload(draft: Mapping[str, Any]) -> dict[str, Any]:
    missing = [field for field in SEND_PAYLOAD_FIELDS if field not in draft]
    if missing:
        raise ValueError(f"EmailDraft lacks send_payload fields: {missing}")
    payload: dict[str, Any] = {field: draft[field] for field in SEND_PAYLOAD_FIELDS}
    payload["payload_version"] = SEND_PAYLOAD_VERSION
    return payload


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def compute_draft_hash(draft: Mapping[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(send_payload(draft))).hexdigest()

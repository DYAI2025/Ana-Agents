"""Offline JSON Schema registry for the Ana contract family (ADR-003).

Guarantees checked at construction time (fail-closed, raises ``SchemaRegistryError``):

- every schema declares Draft 2020-12 and is valid against its metaschema;
- every ``$id`` is local (``BASE_URI`` + file name) and unique;
- every ``$ref`` is local and resolves; no network retrieval exists;
- ``format`` is actively asserted (``date-time``, ``uri``, ``email``), proven by a canary;
- the envelope's ``artifact_type`` enum equals the set of pipeline schemas.
"""

from __future__ import annotations

import functools
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from referencing import Registry
from referencing.exceptions import Unresolvable
from referencing.jsonschema import DRAFT202012

from ana_agents import CONTRACTS_DIR
from ana_agents.contracts import findings as F
from ana_agents.contracts.findings import Finding

DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"
BASE_URI = "https://schemas.ana-agents.invalid/contracts/v1/"
DEFAULT_SCHEMA_DIR = CONTRACTS_DIR / "schemas"
ENVELOPE_TITLE = "ArtifactEnvelope"


class SchemaRegistryError(Exception):
    """The schema set itself is broken. Never caught to produce a green result."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


def _iter_refs(node: Any, pointer: str = "") -> Iterator[tuple[str, str]]:
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str):
                yield pointer, value
            else:
                yield from _iter_refs(value, f"{pointer}/{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _iter_refs(value, f"{pointer}/{index}")


def _json_pointer(parts: Any) -> str:
    return "/" + "/".join(str(p) for p in parts) if parts else ""


class SchemaRegistry:
    def __init__(self, schema_dir: Path = DEFAULT_SCHEMA_DIR) -> None:
        self.schema_dir = Path(schema_dir)
        self.schemas: dict[str, dict[str, Any]] = {}  # title -> schema
        self._ids: dict[str, str] = {}  # $id -> title
        self._load()
        # No `retrieve` callable: any reference outside the loaded resources is Unresolvable.
        self.registry: Registry = Registry().with_resources(
            (schema["$id"], DRAFT202012.create_resource(schema)) for schema in self.schemas.values()
        )
        self._check_refs()
        self.format_checker = Draft202012Validator.FORMAT_CHECKER
        self._check_format_canary()
        self._validators = {
            title: Draft202012Validator(
                schema, registry=self.registry, format_checker=self.format_checker
            )
            for title, schema in self.schemas.items()
        }
        self.pipeline_types = frozenset(
            title for title, s in self.schemas.items() if s.get("x-ana-kind") == "pipeline"
        )
        self._check_envelope_types()

    # -- construction checks -------------------------------------------------------------

    def _load(self) -> None:
        files = sorted(self.schema_dir.glob("*.schema.json"))
        if not files:
            raise SchemaRegistryError("REGISTRY_EMPTY", f"no schemas in {self.schema_dir}")
        for path in files:
            try:
                schema = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise SchemaRegistryError("REGISTRY_INVALID_JSON", f"{path.name}: {exc}") from exc
            if schema.get("$schema") != DRAFT_2020_12:
                raise SchemaRegistryError(
                    "REGISTRY_WRONG_DRAFT", f"{path.name} does not declare Draft 2020-12"
                )
            expected_id = BASE_URI + path.name
            if schema.get("$id") != expected_id:
                raise SchemaRegistryError(
                    "REGISTRY_BAD_ID", f"{path.name}: $id must be {expected_id!r}"
                )
            try:
                Draft202012Validator.check_schema(schema)
            except SchemaError as exc:
                raise SchemaRegistryError(
                    "REGISTRY_INVALID_SCHEMA", f"{path.name}: {exc.message}"
                ) from exc
            title = schema.get("title")
            if not isinstance(title, str) or title in self.schemas:
                raise SchemaRegistryError(
                    "REGISTRY_BAD_TITLE", f"{path.name}: missing or duplicate title {title!r}"
                )
            self.schemas[title] = schema
            self._ids[schema["$id"]] = title

    def _check_refs(self) -> None:
        for title, schema in self.schemas.items():
            resolver = self.registry.resolver(base_uri=schema["$id"])
            for pointer, ref in _iter_refs(schema):
                if "://" in ref and not ref.startswith(BASE_URI):
                    raise SchemaRegistryError(
                        "REGISTRY_NONLOCAL_REF", f"{title}{pointer}: $ref {ref!r} is not local"
                    )
                try:
                    resolver.lookup(ref)
                except Unresolvable as exc:
                    raise SchemaRegistryError(
                        "REGISTRY_UNRESOLVABLE_REF", f"{title}{pointer}: $ref {ref!r} ({exc})"
                    ) from exc

    def _check_format_canary(self) -> None:
        checker = self.format_checker
        missing = {"date-time", "uri", "email"} - set(checker.checkers)
        if missing:
            raise SchemaRegistryError(
                "REGISTRY_FORMAT_CHECK_INACTIVE",
                f"format checkers not active: {sorted(missing)} (install declared dependencies)",
            )
        canaries = [
            ("2026-10-07T12:00:00Z", "date-time", True),
            ("2026-10-07T12:00:00+02:00", "date-time", True),
            ("2026-13-45T25:61:00Z", "date-time", False),
            ("2026-10-07T12:00:00", "date-time", False),  # RFC 3339 requires an offset
            ("2026-10-07", "date-time", False),
            ("https://brand.example.com/about", "uri", True),
            ("not a uri", "uri", False),
        ]
        for value, fmt, expected in canaries:
            if checker.conforms(value, fmt) is not expected:
                raise SchemaRegistryError(
                    "REGISTRY_FORMAT_CHECK_INACTIVE",
                    f"format canary failed: {fmt} {value!r} expected conforms={expected}",
                )

    def _check_envelope_types(self) -> None:
        envelope = self.schemas.get(ENVELOPE_TITLE)
        if envelope is None:
            raise SchemaRegistryError("REGISTRY_MISSING_ENVELOPE", "ArtifactEnvelope missing")
        declared = set(envelope["properties"]["artifact_type"]["enum"])
        if declared != set(self.pipeline_types):
            raise SchemaRegistryError(
                "REGISTRY_ENVELOPE_TYPE_DRIFT",
                f"envelope enum {sorted(declared)} != "
                f"pipeline schemas {sorted(self.pipeline_types)}",
            )

    # -- validation ----------------------------------------------------------------------

    def validate(self, instance: Any, title: str, artifact_id: str | None = None) -> list[Finding]:
        """Validate ``instance`` against the schema named ``title``; return schema findings."""
        validator = self._validators.get(title)
        if validator is None:
            return [
                Finding(
                    F.REGISTRY_UNKNOWN_ARTIFACT_TYPE, artifact_id, "", f"no schema named {title!r}"
                )
            ]
        try:
            errors = sorted(
                validator.iter_errors(instance), key=lambda e: (list(map(str, e.path)), e.validator)
            )
        except Unresolvable as exc:  # pragma: no cover - construction already resolved all refs
            raise SchemaRegistryError("REGISTRY_UNRESOLVABLE_REF", str(exc)) from exc
        if len(errors) > 1:
            errors = [e for e in errors if not self._spurious_unevaluated(e, instance, title)]
        return [
            Finding(
                F.SCHEMA_INVALID,
                artifact_id,
                _json_pointer(error.absolute_path),
                error.message,
                keyword=str(error.validator),
            )
            for error in errors
        ]

    def declared_properties(self, title: str) -> frozenset[str]:
        """Top-level property names declared by a schema and its ``allOf`` references."""
        schema = self.schemas[title]
        names = set(schema.get("properties", {}))
        resolver = self.registry.resolver(base_uri=schema["$id"])
        for part in schema.get("allOf", []):
            if "$ref" in part:
                names |= set(resolver.lookup(part["$ref"]).contents.get("properties", {}))
        return frozenset(names)

    def _spurious_unevaluated(self, error: Any, instance: Any, title: str) -> bool:
        """Draft 2020-12 discards annotations of a failing ``allOf`` branch, so a single
        envelope error also yields an ``unevaluatedProperties`` error that lists declared
        fields. Drop it only when the instance has no undeclared key; a genuine extra key
        is still reported. The artifact fails either way."""
        if error.validator != "unevaluatedProperties" or error.absolute_path:
            return False
        if not isinstance(instance, dict):
            return False
        return set(instance) <= self.declared_properties(title)

    def validate_artifact(self, artifact: Any) -> list[Finding]:
        """Dispatch a pipeline artifact to its schema by ``artifact_type`` (deterministic)."""
        if not isinstance(artifact, dict):
            return [Finding(F.REGISTRY_NOT_AN_OBJECT, None, "", "artifact must be a JSON object")]
        artifact_id = artifact.get("artifact_id")
        artifact_id = artifact_id if isinstance(artifact_id, str) else None
        artifact_type = artifact.get("artifact_type")
        if artifact_type not in self.pipeline_types:
            return [
                Finding(
                    F.REGISTRY_UNKNOWN_ARTIFACT_TYPE,
                    artifact_id,
                    "/artifact_type",
                    f"{artifact_type!r} is not a pipeline artifact type",
                )
            ]
        return self.validate(artifact, artifact_type, artifact_id)


@functools.cache
def default_registry() -> SchemaRegistry:
    return SchemaRegistry()

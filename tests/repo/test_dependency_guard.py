"""Domain portability guard (SYS-003): no provider/framework SDK in the domain package."""

from __future__ import annotations

import tomllib

import pytest

from ana_agents import REPO_ROOT

DOMAIN = REPO_ROOT / "src" / "ana_agents"


@pytest.mark.parametrize(
    "source",
    [
        "import openai",
        "import anthropic as a",
        "from langchain.chains import LLMChain",
        "from langchain_core import messages",
        "import crewai",
        "from autogen import AssistantAgent",
        "import zcrmsdk",
        "def f():\n    import openai.types\n",
    ],
)
def test_guard_detects_forbidden_import(hygiene, source):
    """Canary: the guard must fire on each planted import."""
    found = hygiene.forbidden_imports(source, "planted.py")
    assert [f.code for f in found] == ["HYG_FORBIDDEN_IMPORT"]


@pytest.mark.parametrize(
    "source",
    [
        "import json",
        "from ana_agents.contracts import hashing",
        "x = 'import openai'  # only text",
        "from . import openai",  # relative import of a local module
    ],
)
def test_guard_ignores_allowed_code(hygiene, source):
    assert hygiene.forbidden_imports(source, "ok.py") == []


def test_domain_package_has_no_forbidden_imports(hygiene):
    files = sorted(DOMAIN.rglob("*.py"))
    assert files, "domain package not found"
    found = [f for path in files for f in hygiene.forbidden_imports(path.read_text(), str(path))]
    assert found == []


def test_declared_dependencies_contain_no_provider_sdk(hygiene):
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())
    declared = list(data["project"]["dependencies"])
    for group in data.get("dependency-groups", {}).values():
        declared += group
    roots = {
        dep.split(">")[0]
        .split("<")[0]
        .split("=")[0]
        .split("[")[0]
        .strip()
        .lower()
        .replace("-", "_")
        for dep in declared
    }
    assert roots.isdisjoint(hygiene.FORBIDDEN_IMPORT_ROOTS)

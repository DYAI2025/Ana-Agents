from __future__ import annotations

import copy
import importlib.util
import sys
from typing import Any

import pytest

from ana_agents import CONTRACTS_DIR, REPO_ROOT
from ana_agents.contracts.examples import Chain, load_chain

EXAMPLES = CONTRACTS_DIR / "examples"


@pytest.fixture
def send_chain() -> Chain:
    return load_chain(EXAMPLES / "chains" / "valid-send-chain.json")


@pytest.fixture
def artifacts(send_chain: Chain) -> dict[str, dict[str, Any]]:
    """Deep copies of the valid send chain, keyed by artifact id."""
    return {a["artifact_id"]: copy.deepcopy(a) for a in send_chain.artifacts}


@pytest.fixture(scope="session")
def hygiene():
    """Import scripts/check_repo_hygiene.py as a module."""
    path = REPO_ROOT / "scripts" / "check_repo_hygiene.py"
    spec = importlib.util.spec_from_file_location("check_repo_hygiene", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_repo_hygiene"] = module
    spec.loader.exec_module(module)
    return module

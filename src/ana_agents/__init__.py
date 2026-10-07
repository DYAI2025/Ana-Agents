"""Ana Agents: canonical contracts and deterministic validation foundation (S1).

The domain layer is provider- and framework-agnostic (SPEC SYS-003). Nothing in this
package grants send authority: validators check contract consistency only (ADR-003).
"""

from pathlib import Path

__all__ = ["CONTRACTS_DIR", "REPO_ROOT"]

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACTS_DIR = REPO_ROOT / "contracts"

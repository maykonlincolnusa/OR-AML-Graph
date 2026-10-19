"""Public API for OR AML Graph."""

from .analytics import analyze_transactions, find_cycles
from .temporal import temporal_cycles

__version__ = "0.3.0"


def project_info() -> dict[str, str]:
    return {
        "name": "OR AML Graph",
        "focus": "Explainable graph analysis for AML investigations",
        "status": "reference-prototype",
    }


__all__ = ["analyze_transactions", "find_cycles", "project_info", "temporal_cycles"]


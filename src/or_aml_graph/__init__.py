"""Starter package for OR AML Graph."""

from .analytics import find_cycles

__version__ = "0.1.0"


def project_info() -> dict[str, str]:
    return {
        "name": "OR AML Graph",
        "focus": "Explainable graph analysis for AML investigations",
        "status": "starter",
    }


__all__ = ["find_cycles", "project_info"]


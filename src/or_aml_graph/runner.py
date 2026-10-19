"""Validated boundary used by the CLI and HTTP adapter."""
from .analytics import analyze_transactions
from .temporal import temporal_cycles


def run(payload):
    if not isinstance(payload, dict) or set(payload) - set(["transactions","options","action"]):
        raise ValueError("request must be an object containing only documented fields")
    if payload.get("action") == "temporal":
        return temporal_cycles(payload.get("transactions"), **payload.get("options", {}))
    if payload.get("action", "topology") != "topology":
        raise ValueError("unknown action")
    return analyze_transactions(payload.get('transactions'), **payload.get('options', {}))

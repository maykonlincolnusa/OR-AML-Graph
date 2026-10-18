"""Validated boundary used by the CLI and HTTP adapter."""
from .analytics import analyze_transactions


def run(payload):
    if not isinstance(payload, dict) or set(payload) - set(["transactions","options"]):
        raise ValueError("request must be an object containing only documented fields")
    return analyze_transactions(payload.get('transactions'), **payload.get('options', {}))

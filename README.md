# OR AML Graph

Bounded, explainable graph analytics for anti-money-laundering investigations. The prototype identifies cycles and fan-in/fan-out patterns while preserving the transactions used as evidence.

## Why it matters

Transaction monitoring can miss relationships that become visible only at network level. This project demonstrates graph traversal with operational limits, deterministic results, currency isolation, and explicit caveats. A graph pattern is an investigative lead, not proof of ownership or criminal conduct.

## Current capabilities

- Directed cycle detection with transaction-level evidence.
- Fan-in and fan-out indicators with configurable thresholds.
- Separate analysis for each currency; no implicit FX conversion.
- Maximum depth and expansion budgets with visible truncation.
- Strictly time-ordered cycle detection with bounded elapsed time and evidence.
- Strict input validation, deterministic CLI, optional authenticated API, Docker image, and CI.

## Run

```sh
python -m pip install -e '.[dev,api]'
python -m or_aml_graph --demo
pytest -q && ruff check src tests
```

API: set `OR_API_KEY` to at least 16 characters, run `uvicorn or_aml_graph.api:create_app --factory`, then POST the JSON in `examples/request.json` to `/v1/analyze` with `X-API-Key`.

## Input and output

The request contains `transactions` and optional `options`. Money is represented as decimal strings, timestamps require time zones, and currency codes use three uppercase letters. Results contain one network per currency, cycles, fan patterns, evidence IDs, expansion counts, and truncation status.

## Limitations and roadmap

Set `action` to `temporal` to distinguish a causal sequence from a topology-only cycle. This is a reference prototype with in-process analysis and synthetic examples. It has no identity resolution, beneficial-ownership inference, graph database, sanctions screening, calibrated model, or production observability. Logical next steps are entity-resolution interfaces, benchmark datasets, false-positive measurement, and a graph visualization.

## Responsible use

Use synthetic, public, or properly governed data. Human investigators must verify context and lawful purpose before taking action.

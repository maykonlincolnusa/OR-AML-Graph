from or_aml_graph.temporal import temporal_cycles


def row(identifier, source, target, minute):
    return {"id": identifier, "source_account_id": source,
            "destination_account_id": target, "amount": "1", "currency": "USD",
            "occurred_at": f"2026-01-01T10:{minute:02d}:00Z"}


def test_cycle_requires_strict_time_order():
    ordered = [row("1", "a", "b", 0), row("2", "b", "c", 1), row("3", "c", "a", 2)]
    assert temporal_cycles(ordered)["alerts"][0]["transaction_ids"] == ["1", "2", "3"]
    unordered = [row("1", "a", "b", 2), row("2", "b", "c", 1), row("3", "c", "a", 0)]
    assert temporal_cycles(unordered)["alerts"] == []

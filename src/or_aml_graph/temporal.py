"""Enumerate causal cycles using strictly increasing transfer times."""
from collections import defaultdict
from datetime import timedelta
from hashlib import sha256

from .validation import instant, integer, transactions


def temporal_cycles(rows, max_minutes=60, max_hops=5, max_expansions=10000):
    integer(max_minutes, "max_minutes", 1, 10080)
    integer(max_hops, "max_hops", 2, 10)
    integer(max_expansions, "max_expansions", 1, 100000)
    events = transactions(rows)
    outgoing = defaultdict(list)
    for row in events:
        outgoing[(row["source_account_id"], row["currency"])].append(row)
    alerts, expansions, truncated = [], 0, False
    for seed in events:
        origin = seed["source_account_id"]
        stack = [([seed], [origin, seed["destination_account_id"]])]
        while stack:
            path, accounts = stack.pop()
            for candidate in outgoing[(accounts[-1], seed["currency"])]:
                if expansions >= max_expansions:
                    truncated = True
                    break
                expansions += 1
                when = instant(candidate["occurred_at"])
                if when <= instant(path[-1]["occurred_at"]):
                    continue
                if when - instant(seed["occurred_at"]) > timedelta(minutes=max_minutes):
                    continue
                target = candidate["destination_account_id"]
                extended = path + [candidate]
                if target == origin:
                    ids = [row["id"] for row in extended]
                    alerts.append({"id": "temporal-" + sha256(repr(ids).encode()).hexdigest()[:20],
                                   "rule": "TEMPORAL_CYCLE", "rule_version": "3.0",
                                   "transaction_ids": ids, "account_ids": accounts + [target],
                                   "currency": seed["currency"],
                                   "elapsed_seconds": int((when - instant(seed["occurred_at"])).total_seconds())})
                elif target not in accounts and len(extended) < max_hops:
                    stack.append((extended, accounts + [target]))
            if truncated:
                break
        if truncated:
            break
    return {"alerts": alerts, "truncated": truncated, "expansions": expansions,
            "semantics": "Strict time order supports temporal reachability, not attribution of funds."}

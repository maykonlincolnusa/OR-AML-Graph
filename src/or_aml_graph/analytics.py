"""Bounded topology analysis; cycles are not temporal money attribution."""
from __future__ import annotations

from collections import defaultdict

from .validation import integer, records, text, transactions


def _cycles(rows, max_depth, max_expansions):
    integer(max_depth, "max_depth", 2, 10)
    integer(max_expansions, "max_expansions", 1, 100000)
    adjacency = defaultdict(set)
    for row in records(rows):
        source = text(row.get("source_account_id"), "source_account_id")
        target = text(row.get("destination_account_id"), "destination_account_id")
        if source == target:
            raise ValueError("self transfers are not supported")
        adjacency[source].add(target)
    found, expansions = set(), 0
    for origin in sorted(adjacency):
        stack = [(origin, [origin])]
        while stack:
            current, path = stack.pop()
            for neighbour in sorted(adjacency.get(current, set())):
                if expansions >= max_expansions:
                    return [list(c) + [c[0]] for c in sorted(found)], True, expansions
                expansions += 1
                if neighbour == origin and len(path) >= 2:
                    rotations = [tuple(path[i:] + path[:i]) for i in range(len(path))]
                    found.add(min(rotations))
                elif neighbour not in path and len(path) < max_depth:
                    stack.append((neighbour, path + [neighbour]))
    return [list(c) + [c[0]] for c in sorted(found)], False, expansions


def find_cycles(transactions, max_depth=5, max_expansions=10000):
    cycles, truncated, _ = _cycles(transactions, max_depth, max_expansions)
    if truncated:
        raise ValueError("graph budget exceeded; use analyze_transactions for partial results")
    return cycles


def analyze_transactions(transactions_input, max_depth=5, max_expansions=10000, fan_threshold=3):
    integer(fan_threshold, "fan_threshold", 2)
    grouped = defaultdict(list)
    for row in transactions(transactions_input):
        grouped[row["currency"]].append(row)
    result = []
    remaining = max_expansions
    integer(remaining, "max_expansions", 1, 100000)
    integer(max_depth, "max_depth", 2, 10)
    for unit, rows in sorted(grouped.items()):
        if remaining:
            cycles, truncated, used = _cycles(rows, max_depth, remaining)
            remaining -= used
        else:
            cycles, truncated, used = [], True, 0
        outgoing, incoming = defaultdict(list), defaultdict(list)
        for row in rows:
            outgoing[row["source_account_id"]].append(row)
            incoming[row["destination_account_id"]].append(row)
        findings = []
        for rule, groups, field in [
            ("FAN_OUT", outgoing, "destination_account_id"),
            ("FAN_IN", incoming, "source_account_id"),
        ]:
            for account, events in sorted(groups.items()):
                if len({r[field] for r in events}) >= fan_threshold:
                    findings.append({"rule": rule, "account_id": account,
                                     "transaction_ids": sorted(r["id"] for r in events)})
        cycle_evidence = []
        for cycle in cycles:
            edges = set(zip(cycle, cycle[1:]))
            cycle_evidence.append({
                "accounts": cycle,
                "transaction_ids": sorted(r["id"] for r in rows
                                          if (r["source_account_id"], r["destination_account_id"]) in edges),
            })
        result.append({"currency": unit, "cycles": cycle_evidence, "findings": findings,
                       "truncated": truncated, "expansions": used})
    return {"networks": result, "rule_version": "2.0", "max_cycle_length": max_depth,
            "semantics": "Topology within the supplied dataset; no temporal or beneficial-ownership inference."}


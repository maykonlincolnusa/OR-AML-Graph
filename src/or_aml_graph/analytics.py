"""Dependency-free graph rules for small AML demonstrations."""

from __future__ import annotations

from collections import defaultdict


def find_cycles(transactions: list[dict[str, object]], max_depth: int = 5) -> list[list[str]]:
    adjacency: dict[str, set[str]] = defaultdict(set)
    for row in transactions:
        adjacency[str(row["source_account_id"])].add(str(row["destination_account_id"]))

    found: set[tuple[str, ...]] = set()

    def canonical(cycle: list[str]) -> tuple[str, ...]:
        body = cycle[:-1]
        rotations = [tuple(body[index:] + body[:index]) for index in range(len(body))]
        return min(rotations)

    def walk(origin: str, current: str, path: list[str]) -> None:
        if len(path) > max_depth:
            return
        for neighbour in adjacency.get(current, set()):
            if neighbour == origin and len(path) >= 2:
                found.add(canonical(path + [origin]))
            elif neighbour not in path:
                walk(origin, neighbour, path + [neighbour])

    for node in adjacency:
        walk(node, node, [node])
    return [list(cycle) + [cycle[0]] for cycle in sorted(found)]


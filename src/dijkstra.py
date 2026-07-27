"""Dijkstra shortest path over the {node: [(neighbour, weight), ...]} graphs
produced by src.graph.load_graph.

Uses a heapq with lazy deletion: improved costs are pushed as new entries
and stale entries are skipped when popped.
"""

import heapq


def shortest_path(graph, start, end):
    """Return (path, total_cost) for the cheapest route from start to end.

    path is a list of node names from start to end inclusive.
    Raises ValueError if end is unreachable from start.
    """
    dist = {start: 0}
    prev = {}
    visited = set()
    heap = [(0, start)]

    while heap:
        cost, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        if node == end:
            break
        for neighbour, weight in graph.get(node, []):
            new_cost = cost + weight
            if neighbour not in visited and new_cost < dist.get(neighbour, float("inf")):
                dist[neighbour] = new_cost
                prev[neighbour] = node
                heapq.heappush(heap, (new_cost, neighbour))

    if end not in visited:
        raise ValueError(f"no path from {start!r} to {end!r}")

    path = [end]
    while path[-1] != start:
        path.append(prev[path[-1]])
    path.reverse()
    return path, dist[end]

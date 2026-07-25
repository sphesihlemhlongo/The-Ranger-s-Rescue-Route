"""Graph loading for Rangers Rescue.

Adjacency-list JSON in data/ maps each node name to a list of neighbour
objects. Level 1 neighbours carry a single "weight"; level 2 neighbours
carry "time" and "risk", which are collapsed to weight = time + risk at
parse time so the rest of the code only ever sees (node, weight) pairs.
"""

import json


def load_graph(path, level):
    """Load a graph as {node: [(neighbour, weight), ...]}.

    path: JSON file with {"A": [{"node": "C", "weight": 4}, ...], ...}
          (level 1) or {"A": [{"node": "P1", "time": 3, "risk": 1}, ...], ...}
          (level 2).
    level: 1 uses "weight" directly; 2 uses "time" + "risk".
    """
    if level not in (1, 2):
        raise ValueError(f"unsupported level: {level}")

    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    graph = {}
    for node, neighbours in raw.items():
        edges = []
        for nb in neighbours:
            if level == 1:
                weight = nb["weight"]
            else:
                weight = nb["time"] + nb["risk"]
            edges.append((nb["node"], weight))
        graph[node] = edges
    return graph

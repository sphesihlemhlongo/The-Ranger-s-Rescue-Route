"""Route validation against a {node: [(neighbour, weight), ...]} graph."""


def validate_route(graph, route):
    """Check every consecutive pair in route is a real edge; return total cost.

    Raises ValueError naming the offending pair if any hop is not an edge.
    """
    total = 0
    for a, b in zip(route, route[1:]):
        weights = dict(graph.get(a, []))
        if b not in weights:
            raise ValueError(f"invalid hop: {(a, b)}")
        total += weights[b]
    return total

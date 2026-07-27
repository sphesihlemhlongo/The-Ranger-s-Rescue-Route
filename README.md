# The Ranger's Rescue Route

Solver for the Entelect "Ranger's Rescue Route" challenge: find the cheapest
route from `A` to `B` through a park trail network, validate it, and emit the
answer file for submission.

## Project layout

```
data/               Level input graphs (adjacency-list JSON)
  level1.json       Level 1: edges carry a single "weight"
  level2.json       Level 2: edges carry "time" and "risk" (weight = time + risk)
  level3.json       Level 3 (bonus): 100 nodes, required stops — not solved yet
src/
  graph.py          load_graph(path, level) -> {node: [(neighbour, weight), ...]}
  dijkstra.py       shortest_path(graph, start, end) -> (path, cost)
  validate.py       validate_route(graph, route) -> cost (raises on fake hops)
  solve.py          CLI entry point; writes out/level<N>_answer.json
tests/              pytest suite for graph loading, Dijkstra, and validation
out/                Generated answer files (created on first run)
```

## Setup

Requires Python 3.12+.

```
pip install -r requirements.txt
```

## Usage

Solve level 1 (prints the route, cost, and expected score, and writes
`out/level1_answer.json`):

```
python src/solve.py --level 1
```

The solver independently re-validates the Dijkstra route with
`validate_route` and refuses to write the answer file if validation fails or
disagrees on cost.

## Tests

```
python -m pytest -q
```

## Status

| Level | Status | Notes |
|-------|--------|-------|
| 1 | Solved | `A -> D -> B`, cost 7 |
| 2 | Not implemented | `--level 2` raises `NotImplementedError` |
| 3 | Not started | Bonus level with 24 required stops |

## Implementation notes

- `shortest_path` is Dijkstra with a `heapq` and lazy deletion: improved
  costs are pushed as new heap entries and stale entries are skipped when
  popped. Predecessors are tracked and the path reconstructed by walking
  back from the end node. Unreachable ends raise `ValueError`.
- Level 2 edges collapse to a single weight (`time + risk`) at load time, so
  the rest of the code only ever sees `(node, weight)` pairs.
- The expected score printed by `solve.py` is `optimal_cost / route_cost x 100`.

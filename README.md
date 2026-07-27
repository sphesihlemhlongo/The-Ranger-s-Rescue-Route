# The Ranger's Rescue Route

Solver for the Entelect "Ranger's Rescue Route" challenge: find the cheapest
route from `A` to `B` through a park trail network, validate it, and emit the
answer file for submission.

## Project layout

```
scripts/
  package.py        Build a submission: test, solve, validate, score, zip
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

Solve level 1 (prints the route, cost, and expected score, and writes the
answer to both `out/level1_answer.json` and `out/level1_answer.txt`):

```
python src/solve.py --level 1
```

Current output:

```
route: A -> D -> E -> B
cost: 9
expected score: 100.0  (optimal 9 / cost 9)
```

The solver independently re-validates the Dijkstra route with
`validate_route` and refuses to write the answer file if validation fails or
disagrees on cost.

## Tests

```
python -m pytest -q
```

## Building a submission

`scripts/package.py` is the only supported way to produce a submission:

```
python scripts/package.py --level 1
```

It runs five gates in order and produces no zip if any of them fails:

1. `pytest -q` must be green.
2. Solve the level.
3. Re-validate the answer *file on disk* against the graph — every
   consecutive pair must be a real edge, and the route must run A to B.
4. Score must be exactly 100. Below 100 means a suboptimal route; above 100
   is impossible per the spec and means the graph data is wrong.
5. Zip the source.

Outputs `out/level<N>_answer.json` (upload this) and
`submission_level<N>.zip` (upload this too).

## Status

| Level | Status | Notes |
|-------|--------|-------|
| 1 | Solved, score 100 | `A -> D -> E -> B`, cost 9 (matches the spec optimum) |
| 2 | Not implemented | `--level 2` raises `NotImplementedError`. `data/level2.json` does not match the spec and must be rebuilt first — see `Plan.md`. |
| 3 | Not started | Bonus level with 24 required stops |

## Implementation notes

- `shortest_path` is Dijkstra with a `heapq` and lazy deletion: improved
  costs are pushed as new heap entries and stale entries are skipped when
  popped. Predecessors are tracked and the path reconstructed by walking
  back from the end node. Unreachable ends raise `ValueError`.
- Level 2 edges collapse to a single weight (`time + risk`) at load time, so
  the rest of the code only ever sees `(node, weight)` pairs.
- The expected score printed by `solve.py` is `optimal_cost / route_cost x 100`,
  where `optimal_cost` comes from the `OPTIMA` constants documented in
  `CLAUDE.md` (L1=9, L2=60) — never from our own route, which would make the
  score trivially 100 and unable to detect a suboptimal or invalid answer.

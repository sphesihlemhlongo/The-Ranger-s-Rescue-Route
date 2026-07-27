"""Solve Rangers Rescue levels and write the answer JSON to out/."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.dijkstra import shortest_path
from src.graph import load_graph
from src.validate import validate_route

# Known optima per CLAUDE.md. The scorer computes score = optimal / my_cost * 100,
# so the optimum must come from the spec, never from our own route's cost.
OPTIMA = {1: 9, 2: 60}


def report_score(level, cost):
    """Print the expected score and flag anything that is not exactly 100."""
    optimal = OPTIMA[level]
    score = optimal / cost * 100
    print(f"expected score: {score:.1f}  (optimal {optimal} / cost {cost})")

    if cost > optimal:
        print(
            f"WARNING: route is suboptimal (cost {cost} > optimal {optimal}). "
            "Do not upload below 100."
        )
    elif cost < optimal:
        print(
            f"WARNING: cost {cost} is BELOW the documented optimum {optimal}. "
            "The graph data disagrees with the spec: this route may use edges "
            "that do not exist in the real scorer's graph and would score ZERO. "
            "Verify data/level1.json against the challenge spec before submitting."
        )
    return score


def solve_level1():
    graph = load_graph(ROOT / "data" / "level1.json", level=1)
    route, cost = shortest_path(graph, "A", "B")

    try:
        validated_cost = validate_route(graph, route)
    except ValueError as exc:
        raise SystemExit(f"refusing to write answer: route failed validation: {exc}")
    if validated_cost != cost:
        raise SystemExit(
            f"refusing to write answer: validated cost {validated_cost} != dijkstra cost {cost}"
        )

    print(f"route: {' -> '.join(route)}")
    print(f"cost: {cost}")
    report_score(1, validated_cost)

    out_dir = ROOT / "out"
    out_dir.mkdir(exist_ok=True)
    payload = json.dumps({"route": route}, indent=2)
    # The spec accepts answer.txt or submission.json; write both so the copy
    # that gets uploaded can never lag behind the solver.
    for name in ("level1_answer.json", "level1_answer.txt"):
        out_path = out_dir / name
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(payload + "\n")
        print(f"wrote {out_path.relative_to(ROOT)}")

    return route, validated_cost


def main():
    parser = argparse.ArgumentParser(description="Solve Rangers Rescue levels.")
    parser.add_argument("--level", type=int, choices=(1, 2), required=True)
    args = parser.parse_args()

    if args.level == 1:
        solve_level1()
    else:
        raise NotImplementedError("level 2 is not implemented yet")


if __name__ == "__main__":
    main()

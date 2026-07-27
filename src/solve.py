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

    # Score is optimal_cost / route_cost * 100; our route is the optimum.
    score = cost / validated_cost * 100

    print(f"route: {' -> '.join(route)}")
    print(f"cost: {cost}")
    print(f"expected score: {score:.1f}")

    out_dir = ROOT / "out"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "level1_answer.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"route": route}, f, indent=2)
    print(f"wrote {out_path.relative_to(ROOT)}")


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

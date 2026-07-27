"""Produce a submission for one level, per the Submission Contract in CLAUDE.md.

This is the ONLY supported way to build a submission. It runs every gate in
order and refuses to produce a zip if any of them fails:

  1. pytest -q                     (the whole suite must be green)
  2. solve                         (run the solver for the level)
  3. validate the answer FILE      (re-check the artifact that gets uploaded,
                                    not just the in-memory route)
  4. score                         (must be exactly 100)
  5. zip the source

Usage:  python scripts/package.py --level 1
"""

import argparse
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.graph import load_graph  # noqa: E402
from src.solve import OPTIMA, solve_level1  # noqa: E402
from src.validate import validate_route  # noqa: E402

ENDPOINTS = {1: ("A", "B"), 2: ("A", "B")}

# The contract names README.md + src/ + tests/. data/, conftest.py, pytest.ini
# and requirements.txt are included too because the spec (p.3) requires that a
# reviewer can reproduce the output, and neither `pytest -q` nor
# `python src/solve.py` runs without them.
MANIFEST_FILES = ["README.md", "conftest.py", "pytest.ini", "requirements.txt"]
MANIFEST_DIRS = ["src", "tests", "data"]

EXCLUDED_DIRS = {"__pycache__", ".pytest_cache", ".venv", ".git"}


def fail(stage, message):
    print(f"\nFAILED at stage {stage}: {message}")
    print("No zip produced.")
    raise SystemExit(1)


def stage_tests():
    print("[1/5] running pytest -q")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    if result.returncode != 0:
        fail(1, "test suite is not green")


def stage_solve(level):
    print(f"\n[2/5] solving level {level}")
    if level == 1:
        return solve_level1()
    fail(2, f"level {level} is not implemented yet")


def stage_validate(level):
    """Re-validate the answer file on disk, independently of the solver."""
    print(f"\n[3/5] validating out/level{level}_answer.json")
    answer_path = ROOT / "out" / f"level{level}_answer.json"
    if not answer_path.exists():
        fail(3, f"{answer_path.relative_to(ROOT)} was not written")

    with open(answer_path, encoding="utf-8") as f:
        payload = json.load(f)

    route = payload.get("route")
    if not isinstance(route, list) or not route:
        fail(3, "answer file has no usable 'route' array")

    start, end = ENDPOINTS[level]
    if route[0] != start or route[-1] != end:
        fail(3, f"route must run {start} -> {end}, got {route[0]} -> {route[-1]}")

    graph = load_graph(ROOT / "data" / f"level{level}.json", level=level)
    try:
        cost = validate_route(graph, route)
    except ValueError as exc:
        fail(3, f"answer file contains an invalid hop: {exc}")

    print(f"      route valid: {' -> '.join(route)}")
    print(f"      recomputed cost from graph: {cost}")
    return cost


def stage_score(level, cost):
    print("\n[4/5] scoring")
    optimal = OPTIMA[level]
    score = optimal / cost * 100
    print(f"      local score: {score:.1f}  (optimal {optimal} / cost {cost})")

    if cost > optimal:
        fail(4, f"score {score:.1f} is below 100; never upload a suboptimal route")
    if cost < optimal:
        fail(
            4,
            f"cost {cost} beats the documented optimum {optimal}, which the spec "
            "says is impossible. The graph data is wrong, and this route would "
            "likely score ZERO.",
        )
    return score


def iter_manifest():
    for name in MANIFEST_FILES:
        path = ROOT / name
        if path.exists():
            yield path
    for name in MANIFEST_DIRS:
        for path in sorted((ROOT / name).rglob("*")):
            if not path.is_file():
                continue
            if set(path.relative_to(ROOT).parts) & EXCLUDED_DIRS:
                continue
            if path.suffix == ".pyc":
                continue
            # Skips empty placeholders such as data/level3.json.
            if path.stat().st_size == 0:
                continue
            yield path


def stage_zip(level):
    zip_path = ROOT / f"submission_level{level}.zip"
    print(f"\n[5/5] zipping source -> {zip_path.name}")
    files = list(iter_manifest())

    missing = [n for n in ("README.md",) if not (ROOT / n).exists()]
    if missing:
        fail(5, f"required file(s) missing: {', '.join(missing)}")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, path.relative_to(ROOT).as_posix())
    for path in files:
        print(f"      + {path.relative_to(ROOT).as_posix()}")
    return zip_path


def main():
    parser = argparse.ArgumentParser(description="Build a level submission.")
    parser.add_argument("--level", type=int, choices=(1, 2), required=True)
    args = parser.parse_args()
    level = args.level

    stage_tests()
    stage_solve(level)
    cost = stage_validate(level)
    score = stage_score(level, cost)
    zip_path = stage_zip(level)

    print("\nSUBMISSION READY")
    print(f"  answer file: out/level{level}_answer.json (or .txt)")
    print(f"  source zip:  {zip_path.name}")
    print(f"  local score: {score:.1f}")


if __name__ == "__main__":
    main()

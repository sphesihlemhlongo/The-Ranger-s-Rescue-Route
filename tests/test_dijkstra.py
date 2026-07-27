from pathlib import Path

import pytest

from src.dijkstra import shortest_path
from src.graph import load_graph

DATA = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture(scope="module")
def l1():
    return load_graph(DATA / "level1.json", level=1)


# Spec p.9: optimal_route_cost_L1 = 9. Hand-check: A-D 2 + D-E 3 + E-B 4 = 9.
# Runners-up are A-C-E-B (4+5+4=13) and A-D-E-F-B (2+3+2+7=14).
def test_l1_shortest_a_to_b(l1):
    assert shortest_path(l1, "A", "B") == (["A", "D", "E", "B"], 9)


def test_trivial_same_node(l1):
    assert shortest_path(l1, "A", "A") == (["A"], 0)


# Sub-leg: A-D 2 + D-E 3 = 5, cheaper than the direct A-C-E (4+5=9).
def test_sub_leg_a_to_e(l1):
    assert shortest_path(l1, "A", "E") == (["A", "D", "E"], 5)


def test_unreachable_raises():
    disconnected = {"X": [], "Y": []}
    with pytest.raises(ValueError):
        shortest_path(disconnected, "X", "Y")

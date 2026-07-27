from pathlib import Path

import pytest

from src.dijkstra import shortest_path
from src.graph import load_graph

DATA = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture(scope="module")
def l1():
    return load_graph(DATA / "level1.json", level=1)


# NOTE: data/level1.json has no D-E or E-B edge, so the optimal A->B route
# in the committed data is A-D-B at cost 7 (not A-D-E-B at 9).
def test_l1_shortest_a_to_b(l1):
    assert shortest_path(l1, "A", "B") == (["A", "D", "B"], 7)


def test_trivial_same_node(l1):
    assert shortest_path(l1, "A", "A") == (["A"], 0)


def test_sub_leg_a_to_e(l1):
    assert shortest_path(l1, "A", "E") == (["A", "C", "E"], 7)


def test_unreachable_raises():
    disconnected = {"X": [], "Y": []}
    with pytest.raises(ValueError):
        shortest_path(disconnected, "X", "Y")

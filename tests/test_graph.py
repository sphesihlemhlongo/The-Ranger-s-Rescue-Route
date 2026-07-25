from pathlib import Path

import pytest

from src.graph import load_graph

DATA = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture(scope="module")
def l1():
    return load_graph(DATA / "level1.json", level=1)


@pytest.fixture(scope="module")
def l2():
    return load_graph(DATA / "level2.json", level=2)


def test_l1_known_edges(l1):
    assert ("C", 4) in l1["A"]
    assert ("D", 2) in l1["A"]


def test_l1_symmetry(l1):
    assert ("D", 2) in l1["A"]
    assert ("A", 2) in l1["D"]


def test_l2_collapsed_weights(l2):
    weights = dict(l2["A"])
    assert weights["P6"] == 7  # time 5 + risk 2
    assert weights["P1"] == 4


def test_node_counts(l1, l2):
    assert len(l1) == 6
    assert len(l2) == 18

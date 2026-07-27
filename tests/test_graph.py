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


# Transcribed from the spec PDF p.5, "Edge List (travel time only)". Pinning the
# data to the spec guards against a corrupted data file silently producing a
# wrong-but-plausible answer, which is what happened before.
SPEC_L1_EDGES = {
    frozenset(("A", "C")): 4,
    frozenset(("A", "D")): 2,
    frozenset(("C", "D")): 1,
    frozenset(("C", "E")): 5,
    frozenset(("D", "E")): 3,
    frozenset(("D", "F")): 6,
    frozenset(("E", "F")): 2,
    frozenset(("B", "E")): 4,
    frozenset(("B", "F")): 7,
}


def test_l1_matches_spec_edge_list(l1):
    actual = {
        frozenset((node, nb)): w for node, nbrs in l1.items() for nb, w in nbrs
    }
    assert actual == SPEC_L1_EDGES


@pytest.mark.parametrize("name", ["l1", "l2"])
def test_graph_is_undirected(name, request):
    # Spec: "The graph is undirected - every edge appears in both directions."
    graph = request.getfixturevalue(name)
    for node, neighbours in graph.items():
        for nb, weight in neighbours:
            assert (node, weight) in graph[nb], f"{node}-{nb} missing its reverse"

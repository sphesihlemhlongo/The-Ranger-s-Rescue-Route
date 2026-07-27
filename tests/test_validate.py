from pathlib import Path

import pytest

from src.graph import load_graph
from src.validate import validate_route

DATA = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture(scope="module")
def l1():
    return load_graph(DATA / "level1.json", level=1)


def test_valid_route_cost(l1):
    # The optimal Level 1 route: 2 + 3 + 4 = 9.
    assert validate_route(l1, ["A", "D", "E", "B"]) == 9


def test_suboptimal_but_valid_route(l1):
    # Every hop is a real edge, so this validates; it is just more expensive.
    assert validate_route(l1, ["A", "C", "E", "B"]) == 13


def test_fake_hop_raises_naming_pair(l1):
    # There is no direct A-B trail; the scorer would give this route zero.
    with pytest.raises(ValueError) as exc:
        validate_route(l1, ["A", "B"])
    assert str(("A", "B")) in str(exc.value)

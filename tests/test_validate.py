from pathlib import Path

import pytest

from src.graph import load_graph
from src.validate import validate_route

DATA = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture(scope="module")
def l1():
    return load_graph(DATA / "level1.json", level=1)


def test_valid_route_cost(l1):
    # Optimal A->B route in the committed level 1 data.
    assert validate_route(l1, ["A", "D", "B"]) == 7


def test_fake_hop_raises_naming_pair(l1):
    with pytest.raises(ValueError) as exc:
        validate_route(l1, ["A", "B"])
    assert str(("A", "B")) in str(exc.value)

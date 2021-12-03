import pytest

from jsim.Simulation import Simulation


@pytest.fixture
def simulation():
    Simulation.__abstractmethods__ = set()
    s = Simulation()
    yield s


def test_Simulation_is_properly_abstract():
    abstract_methods = frozenset({"reset", "steps"})
    assert Simulation.__abstractmethods__ - abstract_methods == frozenset()
    assert abstract_methods - Simulation.__abstractmethods__ == frozenset()

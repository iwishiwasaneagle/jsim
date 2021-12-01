import pytest

from jsim.Agent import Agent


@pytest.fixture
def agent():
    Agent.__abstractmethods__ = set()
    a = Agent()
    yield a


def test_Agent_is_properly_abstract():
    abstract_methods = frozenset({"step", "start_trial", "__init__"})
    assert Agent.__abstractmethods__ - abstract_methods == frozenset()
    assert abstract_methods - Agent.__abstractmethods__ == frozenset()

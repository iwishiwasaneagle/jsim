import pytest

from jsim.Environment import Environment


@pytest.fixture
def environment():
    Environment.__abstractmethods__ = set()
    e = Environment()
    yield e


def test_Environment_is_properly_abstract():
    abstract_methods = frozenset({"step", "reset", "__init__"})
    assert Environment.__abstractmethods__ - abstract_methods == frozenset()
    assert abstract_methods - Environment.__abstractmethods__ == frozenset()

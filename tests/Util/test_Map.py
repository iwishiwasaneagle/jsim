import string
import tempfile

import numpy as np
import pytest

from jsim.Util.Map import Map


@pytest.fixture
def _Map():
    Map.__abstractmethods__ = set()
    yield Map


@pytest.fixture
def _map(_Map):
    fd, path = tempfile.mkstemp(suffix=".txt")
    yield _Map(path)


def test_map_invalid(_Map):
    with pytest.raises(FileNotFoundError):
        _Map("".join(np.random.choice(list(string.ascii_letters), size=(10,))) + ".tif")


def test_map_valid(_Map):
    fd, path = tempfile.mkstemp(suffix=".txt")
    _Map(path)


@pytest.mark.parametrize("crs", (None, 1337, False))
def test_set_crs(_map, crs):
    with pytest.raises(TypeError):
        _map.set_crs(crs)

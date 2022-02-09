import pytest

from jsim.Util import VectorMap


@pytest.fixture
def vectormap():
    try:
        yield VectorMap("tests/Util/test.gpkg")
    except FileNotFoundError:
        yield VectorMap("Util/test.gpkg")


@pytest.mark.parametrize("x,y,expected", [(0.1, 0.1, 10), (9.9, 9.9, 10), (5, 5, 10)])
def test_vector_map_getitem(vectormap, x, y, expected):
    actual = vectormap[x, y]["test_val"]
    assert actual == expected  # hard coded in file


def test_vector_map_property(vectormap):
    assert vectormap.gdf is vectormap._map


def test_vector_map_str(vectormap):
    assert vectormap.__str__() == vectormap.__repr__()

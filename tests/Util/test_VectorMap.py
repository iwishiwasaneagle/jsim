import pytest

from jsim.Util import VectorMap


@pytest.fixture
def vectormap():
    try:
        yield VectorMap("tests/Util/test.gpkg")
    except FileNotFoundError:
        yield VectorMap("Util/test.gpkg")


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (0.1, 0.1, [10]),
        (9.9, 9.9, [10]),
        (5, 5, [10]),
        ((0.1, 9.9, 5), (0.1, 9.9, 5), [10.0, 10.0, 10.0]),
    ],
)
def test_vector_map_getitem(vectormap, x, y, expected):
    actual = [int(f) for f in vectormap[x, y]["test_val"]]
    assert actual == expected  # hard coded in file


def test_vector_map_property(vectormap):
    assert vectormap.gdf is vectormap._map


def test_vector_map_str(vectormap):
    assert vectormap.__str__() == vectormap.__repr__()


@pytest.mark.parametrize("crs", ("epsg:27700", "epsg:4326"))
def test_vector_map_set_crs(vectormap, crs):
    vectormap.gdf.crs = None
    vectormap.set_crs(crs)
    assert vectormap.gdf.crs == crs

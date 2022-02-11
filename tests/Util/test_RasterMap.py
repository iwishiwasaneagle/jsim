import numpy as np
import pytest
from rasterio.windows import Window

from jsim.Util import RasterMap


@pytest.fixture
def raster():
    try:
        yield RasterMap("tests/Util/test.tif")
    except FileNotFoundError:
        yield RasterMap("Util/test.tif")


def test_raster_map_valid(raster):
    kwds = raster._map.profile
    assert kwds["height"] == 100
    assert kwds["width"] == 100

    assert kwds["driver"] == "GTiff"

    assert kwds["nodata"] == -9999.0

    assert kwds["count"] == 1


def test_raster_map_str_and_repr(raster):
    assert repr(raster) == str(raster)


def test_raster_map_bounds(raster):
    assert raster.bounds.left == 195000
    assert raster.bounds.bottom == 625000
    assert raster.bounds.right == 200000
    assert raster.bounds.top == 630000


@pytest.mark.parametrize("x,y", [(0, 1), (99, 99), (50, 50)])
def test_raster_map_getitem_int(raster, x, y):
    expected = raster._nd_map[x, y]
    for act, exp in zip(raster[x, y], [expected]):
        assert np.isclose(act, exp)


@pytest.mark.parametrize("x,y", [((0, 1, 2, 3), (0, 1, 2, 3))])
def test_raster_map_getitem_arr(raster, x, y):
    expected = raster._nd_map[x, y]
    for act, exp in zip(raster[x, y], expected):
        assert np.isclose(act, exp)


@pytest.mark.parametrize("x,y", [(-10, 1), (101, 99), (-1, 101)])
def test_raster_map_getitem_int_invalid(raster, x, y):
    for act in raster[x, y]:
        assert act == raster._map.nodata


@pytest.mark.parametrize(
    "row,col,xt,yt",
    [
        (0, 1, 195075.0, 629975.0),
        (95, 99, 199975.0, 625225.0),
        (50, 50, 197525.0, 627475.0),
        (
            (0, 95, 50),
            (1, 99, 50),
            (195075.0, 199975.0, 197525.0),
            (629975.0, 625225.0, 627475.0),
        ),
    ],
)
def test_raster_map_xy(raster, row, col, xt, yt):
    xt_a, yt_a = np.array(raster.xy(row, col))
    assert np.allclose(xt_a, xt)
    assert np.allclose(yt_a, yt)

    assert np.all(xt_a > raster.bounds.left) and np.all(xt_a <= raster.bounds.right)
    assert np.all(yt_a > raster.bounds.bottom) and np.all(yt_a <= raster.bounds.top)


def test_raster_map_shape(raster):
    assert raster.shape == (100, 100)


def test_raster_map_read(raster):
    actual = raster.read(1)
    expected = raster._nd_map
    assert np.all(actual == expected)

    actual = raster.read(window=Window(1000, 1000, 10, 10))
    expected = expected[1000 : 1000 + 10, 1000 : 1000 + 10]

    assert np.all(actual == expected)


@pytest.mark.parametrize(
    "crs,contains",
    (("epsg:27700", "6377563.396,299.324964"), ("epsg:4326", "6378137,298.257223563")),
)
def test_raster_map_set_crs(raster, crs, contains):
    raster.set_crs(crs)
    assert contains in raster._map.crs.wkt

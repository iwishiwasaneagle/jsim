import string

import numpy as np
import pytest

from jsim.Util import RasterMap


@pytest.fixture
def raster():
    yield RasterMap("test.tif")


def test_raster_map_invalid():
    with pytest.raises(FileNotFoundError):
        RasterMap(
            "".join(np.random.choice(list(string.ascii_letters), size=(10,))) + ".tif"
        )


def test_raster_map_valid(raster):
    kwds = raster._map.profile
    assert kwds["height"] == 100
    assert kwds["width"] == 100

    assert kwds["driver"] == "GTiff"

    assert kwds["nodata"] is None

    assert kwds["count"] == 1


def test_raster_map_str_and_repr(raster):
    assert repr(raster) == str(raster)


def test_raster_map_bounds(raster):
    assert raster.bounds.left == 0.0
    assert raster.bounds.bottom == 100.0
    assert raster.bounds.right == 100.0
    assert raster.bounds.top == 0.0


@pytest.mark.parametrize("x,y", [(0, 1), (99, 99), (50, 50)])
def test_raster_map_getitem(raster, x, y):
    assert raster[x, y] == raster._nd_map[x, y]


@pytest.mark.parametrize(
    "row,col,xt,yt",
    [
        (0, 1, 1.5, 0.5),
        (95, 99, 99.5, 95.5),
        (50, 50, 50.5, 50.5),
        ((0, 95, 50), (1, 99, 50), (1.5, 99.5, 50.5), (0.5, 95.5, 50.5)),
    ],
)
def test_raster_map_xy(raster, row, col, xt, yt):
    xt_a, yt_a = raster.xy(row, col)
    assert np.allclose(xt_a, xt)
    assert np.allclose(yt_a, yt)

import pytest

from jsim.Environment.HexEnvironment.HexCoords import PixelCoord


@pytest.fixture
def pixel():
    yield PixelCoord(x=1.0, y=1.0)


def test_axial_coord_works(pixel: PixelCoord):
    assert pixel.x == 1.0
    assert pixel.x == 1.0

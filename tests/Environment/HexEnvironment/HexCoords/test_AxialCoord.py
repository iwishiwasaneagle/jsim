import pytest

from jsim.Environment.HexEnvironment.HexCoords import AxialCoord


@pytest.fixture
def axial():
    yield AxialCoord(q=1.0, r=1.0)


def test_axial_coord_works(axial: AxialCoord):
    assert axial.q == 1.0
    assert axial.r == 1.0

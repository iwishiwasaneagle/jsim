import pytest

from jsim.Environment.HexEnvironment.HexCoords import OffsetCoord


@pytest.fixture
def offset():
    yield OffsetCoord(col=1.0, row=1.0)


def test_offset_coord_works(offset: OffsetCoord):
    assert offset.col == 1.0
    assert offset.row == 1.0

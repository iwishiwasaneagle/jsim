import copy

import numpy as np
import pytest

from jsim.Environment import HexDirections, HexEnvironment
from jsim.Environment.HexEnvironment.HexCoords import (
    AxialCoord,
    OffsetCoord,
    PixelCoord,
)

M = 5


@pytest.fixture
def hexenv():
    nonabs_hexenv = copy.copy(HexEnvironment)
    nonabs_hexenv.__abstractmethods__ = set()
    yield nonabs_hexenv(m=M)


def test_shape(hexenv: HexEnvironment):
    assert hexenv.shape == (M, M)


@pytest.mark.parametrize(
    "test,expected",
    [
        ((0, 0), (0, 0)),
        ((-2, -2), (-2, -1)),
        ((1, 2), (1, 2)),
        ((-2, 0), (-2, 1)),
        ((-2, 2), (-2, 3)),
    ],
)
def test_offset_to_axial(test, expected):
    assert HexEnvironment.offset_to_axial(
        OffsetCoord(col=test[0], row=test[1])
    ) == AxialCoord(q=expected[0], r=expected[1])


@pytest.mark.parametrize(
    "test,expected",
    [
        ((0, 0), (0, 0)),
        ((-2, -1), (-2, -2)),
        ((1, 2), (1, 2)),
        ((-2, 1), (-2, 0)),
        ((-2, 3), (-2, 2)),
    ],
)
def test_axial_to_offset(test, expected):
    assert HexEnvironment.axial_to_offset(
        AxialCoord(q=test[0], r=test[1])
    ) == OffsetCoord(col=expected[0], row=expected[1])


@pytest.mark.parametrize(
    "test,expected",
    [
        ((2, 3), (1.732, 4.000)),
        ((-4, -2), (-3.464, -4.000)),
        ((4, 4), (3.464, 6.000)),
        ((-5, 0), (-4.330, -2.500)),
        ((0, -2), (0.000, -2.000)),
        ((1, 0), (0.866, 0.500)),
        ((-4, 4), (-3.464, 2.000)),
    ],
)
def test_axial_to_pixel(test, expected):
    t = HexEnvironment.axial_to_pixel(AxialCoord(q=test[0], r=test[1]), np.sqrt(1 / 3))
    e = PixelCoord(x=expected[0], y=expected[1])

    assert pytest.approx(t.x, 0.001) == e.x
    assert pytest.approx(t.y, 0.001) == e.y


@pytest.mark.parametrize(
    "test,expected",
    [
        ((-4, 1.0), (-3.464, 1.000)),
        ((-3, -6.0), (-2.598, -5.500)),
        ((-5, -8.0), (-4.330, -7.500)),
        ((4, 4.0), (3.464, 4.000)),
        ((3, 3.0), (2.598, 3.500)),
        ((-5, -1.0), (-4.330, -0.500)),
        ((3, -2.0), (2.598, -1.500)),
    ],
)
def test_offset_to_pixel(test, expected):
    t = HexEnvironment.offset_to_pixel(
        OffsetCoord(col=test[0], row=test[1]), np.sqrt(1 / 3)
    )
    e = PixelCoord(x=expected[0], y=expected[1])

    assert pytest.approx(t.x, 0.001) == e.x
    assert pytest.approx(t.y, 0.001) == e.y


@pytest.mark.parametrize(
    "test,expected",
    [
        # Even col, any row
        ((HexDirections.br, (0, 0)), (1, 0)),
        ((HexDirections.tr, (0, 0)), (1, -1)),
        ((HexDirections.t, (0, 0)), (0, -1)),
        ((HexDirections.tl, (0, 0)), (-1, -1)),
        ((HexDirections.bl, (0, 0)), (-1, 0)),
        ((HexDirections.b, (0, 0)), (0, 1)),
        # Odd col, any row
        ((HexDirections.br, (1, 0)), (2, 1)),
        ((HexDirections.tr, (1, 0)), (2, 0)),
        ((HexDirections.t, (1, 0)), (1, -1)),
        ((HexDirections.tl, (1, 0)), (0, 0)),
        ((HexDirections.bl, (1, 0)), (0, 1)),
        ((HexDirections.b, (1, 0)), (1, 1)),
    ],
)
def test_neighbor_coord(test, expected):
    d, p = test
    pos = OffsetCoord(col=p[0], row=p[1])
    exp = OffsetCoord(col=expected[0], row=expected[1])
    assert HexEnvironment.neighbor_coord(pos, d) == exp


@pytest.mark.parametrize(
    "test,expected",
    [
        ((0, 0), [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (0, 1)]),
        ((1, 0), [(2, 1), (2, 0), (1, -1), (0, 0), (0, 1), (1, 1)]),
    ],
)
def test_neighbors_coord(test, expected):
    pos = OffsetCoord(col=test[0], row=test[1])
    exp = [OffsetCoord(col=e[0], row=e[1]) for e in expected]
    assert HexEnvironment.neighbors_coord(pos) == exp


@pytest.mark.parametrize(
    "test,expected",
    [
        (((0, -2), (-3, -4)), 5.0),
        (((-5, 1), (-1, 3)), 6.0),
        (((-2, -2), (0, 4)), 8.0),
        (((1, -2), (0, 0)), 2.0),
    ],
)
def test_axial_distance_between_a_b(test, expected):
    a, b = test
    a = AxialCoord(q=a[0], r=a[1])
    b = AxialCoord(q=b[0], r=b[1])

    assert HexEnvironment.axial_distance_between_a_b(a, b) == expected


@pytest.mark.parametrize(
    "test,expected",
    [
        (((0, -2), (-3, -4)), 5.0),
        (((-5, 1), (-1, 3)), 6.0),
        (((-2, -2), (0, 4)), 8.0),
        (((1, -2), (0, 0)), 2.0),
    ],
)
def test_distance_between_a_b(test, expected):
    a, b = test
    a = HexEnvironment.axial_to_offset(AxialCoord(q=a[0], r=a[1]))
    b = HexEnvironment.axial_to_offset(AxialCoord(q=b[0], r=b[1]))

    assert HexEnvironment.distance_between_a_b(a, b) == expected

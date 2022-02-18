import numpy as np
import pytest

from jsim.Types import Coord, Coords


@pytest.fixture
def coords(request) -> Coords:
    yield Coords(coords=[Coord(x=x, y=y) for x, y in zip(*request.param)])


@pytest.mark.parametrize(
    "coords,length",
    [
        [((0, 1, 2, 3, 4), (0, 0, 0, 0, 0)), 4],
        [((0, 0, 0, 0, 0), (0, 1, 2, 3, 4)), 4],
        [
            ((20, 30, 40, 50, 60, 70, 80, 90), (20, 30, 40, 50, 60, 70, 80, 90)),
            98.99494936611666,
        ],
        [
            (
                (20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120),
                (-100, -90, -80, -70, -60, -50, -40, -30, -20, -10, 0),
            ),
            141.4213562373095,
        ],
    ],
    indirect=["coords"],
)
def test_distance(coords, length):
    assert np.isclose(coords.distance, length)


@pytest.mark.parametrize(
    "coords,expected_arr",
    [
        [
            ((0, 1, 2, 3, 4), (0, 0, 0, 0, 0)),
        ]
        * 2,
        [
            ((0, 0, 0, 0, 0), (0, 1, 2, 3, 4)),
        ]
        * 2,
        [
            ((20, 30, 40, 50, 60, 70, 80, 90), (20, 30, 40, 50, 60, 70, 80, 90)),
        ]
        * 2,
        [
            (
                (20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120),
                (-100, -90, -80, -70, -60, -50, -40, -30, -20, -10, 0),
            ),
        ]
        * 2,
    ],
    indirect=["coords"],
)
def test_getitem(coords, expected_arr):
    for i, _ in enumerate(expected_arr[0]):
        assert coords[i] == Coord(x=expected_arr[0][i], y=expected_arr[1][i])


@pytest.mark.parametrize(
    "coords,length",
    [
        [((0, 1, 2, 3, 4), (0, 0, 0, 0, 0)), 5],
        [((0, 0, 0, 0, 0), (0, 1, 2, 3, 4)), 5],
        [((20, 30, 40, 50, 60, 70, 80, 90), (20, 30, 40, 50, 60, 70, 80, 90)), 8],
        [
            (
                (20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120),
                (-100, -90, -80, -70, -60, -50, -40, -30, -20, -10, 0),
            ),
            11,
        ],
    ],
    indirect=["coords"],
)
def test_len(coords, length):
    assert len(coords) == length


@pytest.mark.parametrize(
    "coords,append",
    [
        [((0, 0), (1, 1)), Coord(x=2, y=2)],
        [((0, 0, 1), (0, 0, 0)), Coord(x=8, y=8)],
    ],
    indirect=["coords"],
)
def test_append(coords, append):
    coords.append(append)
    assert coords[-1] == append

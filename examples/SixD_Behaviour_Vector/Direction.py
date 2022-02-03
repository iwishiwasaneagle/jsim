from enum import IntEnum

from Coord import Coord

from jsim.Meta import Action


class Direction(Action, IntEnum):
    tl = 0
    t = 1
    tr = 2
    l = 3  # noqa: E741
    sp = 4
    r = 5
    bl = 6
    b = 7
    br = 8

    @staticmethod
    def dir_to_coord(d: "Direction") -> Coord:
        lookup = {
            Direction.tl: (-1, 1),
            Direction.t: (0, 1),
            Direction.tr: (1, 1),
            Direction.l: (-1, 0),
            Direction.sp: (0, 0),
            Direction.r: (1, 0),
            Direction.bl: (-1, -1),
            Direction.b: (0, -1),
            Direction.br: (1, -1),
        }
        x, y = lookup[d]
        return Coord(x=x, y=y)


if __name__ == "__main__":
    assert len([Direction(f) for f in range(9)]) == 9

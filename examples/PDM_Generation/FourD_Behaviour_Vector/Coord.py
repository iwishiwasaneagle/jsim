import pydantic

from jsim.Meta import State


class Coord(pydantic.BaseModel, State):
    x: int
    y: int

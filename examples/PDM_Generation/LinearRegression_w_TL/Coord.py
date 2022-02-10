from pydantic import BaseModel


class Coord(BaseModel):
    x: int
    y: int

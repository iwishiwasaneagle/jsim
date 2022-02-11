from pydantic import BaseModel


class Coord(BaseModel):
    x: float
    y: float

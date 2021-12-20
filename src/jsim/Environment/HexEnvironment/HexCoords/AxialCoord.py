from pydantic import BaseModel


class AxialCoord(BaseModel):
    q: int
    r: int

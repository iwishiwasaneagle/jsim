from pydantic import BaseModel


class OffsetCoord(BaseModel):
    col: int
    row: int

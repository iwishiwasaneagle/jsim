from pydantic import BaseModel


class PixelCoord(BaseModel):
    x: float
    y: float

import os
from typing import Iterable, Union

import rasterio as rio
import rasterio.coords as riocoords
import rasterio.transform as riotrans


class RasterMap:
    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise FileNotFoundError(f'file "{path}" does not exist ({os.getcwd()=})')

        self._map: rio.DatasetReader = rio.open(path)
        self._nd_map = self._map.read(1)

    @property
    def bounds(self) -> riocoords.BoundingBox:
        return self._map.bounds

    def __repr__(self):
        return f"{self.__class__.__name__}\
        (width={self._map.profile['width']}, \
        height={self._map.profile['height']})"

    def __str__(self):
        return self.__repr__()

    def __getitem__(
        self,
        xy: tuple[Union[slice, int, Iterable[int]], Union[slice, int, Iterable[int]]],
    ) -> float:
        x, y = xy
        return self._nd_map[x, y]

    def xy(
        self, row: Union[float, list[float]], col: Union[float, list[float]]
    ) -> Iterable[float]:
        if not isinstance(row, Iterable):
            row = [row]
        if not isinstance(col, Iterable):
            col = [col]

        return riotrans.xy(self._map.profile["transform"], row, col)


if __name__ == "__main__":
    rmap = RasterMap(
        path="../../../examples/SixD_Behaviour_Vector/5m_arran_b_merged.tif"
    )

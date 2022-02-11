from __future__ import annotations

import tempfile
from typing import Iterable, Iterator, List, Tuple, Union

import numpy as np
import rasterio as rio
import rasterio.coords as riocoords
import rasterio.transform as riotrans
import rasterio.warp as riowarp

from jsim.Types import (
    LIST_AND_INDIVIDUAL_COORD,
    LIST_AND_INDIVIDUAL_FLOAT,
    LIST_AND_INDIVIDUAL_INT,
)
from jsim.Util.Map import Map


class RasterMap(Map):
    def __init__(self, path: str):
        super().__init__(path)

        self._map: rio.DatasetReader = rio.open(self.path)
        self._nd_map = self._map.read(1)

    @property
    def bounds(self) -> riocoords.BoundingBox:
        return self._map.bounds

    @property
    def shape(self) -> Tuple[int, int]:
        return self._nd_map.shape

    @property
    def width(self) -> int:
        return self._map.width

    @property
    def height(self) -> int:
        return self._map.height

    def read(self, *args, **kwargs) -> np.ndarray:
        return self._map.read(*args, **kwargs)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"width={self._map.profile['width']}, "
            f"height={self._map.profile['height']})"
        )

    def set_crs(self, crs: str) -> RasterMap:
        super(RasterMap, self).set_crs(crs)
        self_crs = self._map.crs
        transform, width, height = riowarp.calculate_default_transform(
            self_crs, crs, self.width, self.height, *self.bounds
        )
        kwargs = self._map.meta.copy()

        kwargs.update(
            {"crs": crs, "transform": transform, "width": width, "height": height}
        )

        _, w_path = tempfile.mkstemp(suffix=".tif")

        with rio.open(w_path, "w", **kwargs) as dst:
            for i in range(1, self._map.count + 1):
                riowarp.reproject(
                    source=rio.band(self._map, i),
                    destination=rio.band(dst, i),
                    src_transform=self._map.transform,
                    src_crs=self._map.crs,
                    dst_transform=transform,
                    dst_crs=crs,
                    resampling=riowarp.Resampling.nearest,
                )

        self._map.close()
        self._map = rio.open(w_path)

        return self

    def __str__(self):
        return self.__repr__()

    def __getitem__(
        self,
        xy: Tuple[Union[int, Iterable[int]], Union[int, Iterable[int]]],
    ) -> Iterator[float]:
        x, y = xy
        if not isinstance(x, Iterable):
            x = [x]
        if not isinstance(y, Iterable):
            y = [y]

        for xi, yi in zip(x, y):
            if xi < 0 or yi < 0 or xi >= self._map.height or yi >= self._map.width:
                yield self._map.nodata
            else:
                yield self._nd_map[xi, yi]

    def xy(
        self, row: Union[float, List[float]], col: Union[float, List[float]]
    ) -> Iterable[float]:
        pass
        return self._xy(row, col, self._map.profile["transform"])

    @staticmethod
    def _xy(
        row: Union[float, List[float]],
        col: Union[float, List[float]],
        trans: riotrans.Affine,
    ) -> Iterable[float]:
        if not isinstance(row, Iterable):
            row = [row]
        if not isinstance(col, Iterable):
            col = [col]

        return riotrans.xy(trans, row, col)

    def at(
        self,
        x: LIST_AND_INDIVIDUAL_INT = None,
        y: LIST_AND_INDIVIDUAL_INT = None,
        coord: LIST_AND_INDIVIDUAL_COORD = None,
    ) -> LIST_AND_INDIVIDUAL_FLOAT:
        pass

    def _at_xy(
        self, x: LIST_AND_INDIVIDUAL_INT, y: LIST_AND_INDIVIDUAL_INT
    ) -> LIST_AND_INDIVIDUAL_INT:
        pass

    def _at_coord(self, coord: LIST_AND_INDIVIDUAL_COORD) -> LIST_AND_INDIVIDUAL_FLOAT:
        pass


if __name__ == "__main__":
    rmap = RasterMap(
        path="examples/PDM_Generation/SixD_Behaviour_Vector/5m_arran_b_merged.tif"
    )

    rmap.read(1)

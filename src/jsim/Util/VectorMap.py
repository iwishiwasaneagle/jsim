from __future__ import annotations

from typing import Any

import geopandas as gpd
import numpy as np
from shapely.geometry import Point

from jsim.Types import (
    LIST_AND_INDIVIDUAL_COORD,
    LIST_AND_INDIVIDUAL_FLOAT,
    LIST_AND_INDIVIDUAL_INT,
)
from jsim.Util.Map import Map


class VectorMap(Map):
    def __init__(self, path: str):
        super(VectorMap, self).__init__(path)

        self._map: gpd.GeoDataFrame = gpd.read_file(self.path)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__hash__()})"

    def __str__(self):
        return self.__repr__()

    @property
    def gdf(self) -> gpd.GeoDataFrame:
        return self._map

    def __getitem__(self, item):
        return self._getitem(item, self._map)

    def set_crs(self, crs: str) -> VectorMap:
        super(VectorMap, self).set_crs(crs)
        self._map.set_crs(crs, inplace=True)
        return self

    @staticmethod
    def _getitem(item: Any, rmap: gpd.GeoDataFrame):
        item = np.array(item)

        if np.ndim(item) > 1:
            pts = item.T.astype(float).tolist()
        else:
            pts = [(float(item[0]), float(item[1]))]

        return rmap.loc[
            rmap.sindex.query_bulk((Point(*f) for f in pts), "within")[1].tolist()
        ]

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
    v = VectorMap(path="tests/Util/test.gpkg")
    v[5, 5]

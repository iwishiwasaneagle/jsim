from typing import Any

import geopandas as gpd
import numpy as np
from shapely.geometry import Point

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


if __name__ == "__main__":
    v = VectorMap(path="tests/Util/test.gpkg")
    v[5, 5]

import geopandas as gpd
from shapely.geometry import Point

from jsim.Util.Map import Map


class VectorMap(Map):
    def __init__(self, path: str):
        super(VectorMap, self).__init__(path)

        self._map: gpd.GeoDataFrame = gpd.read_file(self.path)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._map.bounds})"

    def __str__(self):
        return self.__repr__()

    @property
    def gdf(self) -> gpd.GeoDataFrame:
        return self._map

    def __getitem__(self, item):
        assert len(item) == 2
        return self._map.loc[int(self._map.sindex.query(Point(*item), "within")[0])]


if __name__ == "__main__":
    v = VectorMap(path="tests/Util/test.gpkg")
    v[5, 5]

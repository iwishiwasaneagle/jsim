import os.path
from typing import Tuple

import numpy as np
import pydantic
import rasterio as rio
import rasterio.transform as riotrans
import skimage as ski
from Coord import Coord
from Vicinity import Vicinity

from jsim.Environment import Environment


class SixDEnv(Environment):
    def __init__(self, slope: str, psim):
        self.psim = psim

        self.slope = rio.open(slope)

        edges_file_path = os.path.splitext(slope)[0] + "_canny.tif"
        if not os.path.exists(edges_file_path):
            kwd = self.slope.profile
            with rio.open(edges_file_path, "w", **kwd) as f:
                edges = ski.feature.canny(self.slope.read(1), sigma=1).astype(int)
                f.write(edges, 1)
        self.edges = rio.open(edges_file_path)

    @pydantic.validate_arguments
    def get_edges_vicinity(self, coord: Coord) -> Vicinity:
        return self._get_vicinity(coord, self.edges)

    @pydantic.validate_arguments
    def get_slope_vicinity(self, coord: Coord) -> Vicinity:
        return self._get_vicinity(coord, self.slope)

    @pydantic.validate_arguments(config=dict(arbitrary_types_allowed=True))
    def _get_vicinity(self, coord: Coord, dataset: rio.DatasetReader) -> Vicinity:
        xs, ys = np.meshgrid(np.arange(-1, 2), np.arange(-1, 2)[::-1])
        xs, ys = xs.flatten(), ys.flatten()
        xs += coord.x
        ys += coord.y

        xs, ys = riotrans.xy(dataset.profile["transform"], xs, ys)
        vicinity = [float(f) for f in dataset.sample(np.vstack((xs, ys)).T)]

        return Vicinity(vicinity=list(vicinity))

    def reset(self, agent_p: Coord) -> Tuple[Vicinity, Vicinity]:
        return self.get_edges_vicinity(agent_p), self.get_slope_vicinity(agent_p)

    def step(self, pa: Coord) -> Tuple[Tuple[Vicinity, Vicinity], float]:
        return (self.get_edges_vicinity(pa), self.get_slope_vicinity(pa)), 0


if __name__ == "__main__":
    env = SixDEnv("./5m_arran_b_merged_slope.tif", None)
    env.get_edges_vicinity(Coord(x=1900, y=2000))

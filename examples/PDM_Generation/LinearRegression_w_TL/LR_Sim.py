import copy
from typing import List

import matplotlib.contour
import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as np
from Coord import Coord
from loguru import logger
from LR_Env import LR_Env
from tqdm.autonotebook import tqdm

from examples.PDM_Generation.LinearRegression_w_TL.VicinityState import (
    VICINITY_DISTS,
    VICINITY_INDICES,
    VicinityState,
)
from jsim.Simulation import Simulation


class LRConsts:
    q0: float = 4.786872732767515
    q1: float = 0.013315859975442301
    q2: float = 0.0019411657191748125
    q3: float = -16.319148163916193
    q4: float = -0.026739066247719285
    q5: float = 0.5717657455052271


class LR_Sim(Simulation):
    env: LR_Env

    active: List[List[int]]
    times: List[List[float]]
    distance: List[List[float]]

    start_height: float
    start: Coord

    def __init__(
        self, dem: str, slope: str, lcid: str, start: Coord = Coord(x=2500, y=2000)
    ):
        self.start = copy.deepcopy(start)
        self.env = LR_Env(self.start, 5, dem, slope, lcid)
        self.reset()

    @staticmethod
    def time_to_cross(v: VicinityState, dists: List[float]) -> float:
        """
        lcid_    - land cover id value
        dem      - elevation above sea level in m
        absslope - absolute value of segment slope tangent
        elev     - difference in elevation between and start point
        dist     - distance walked in m
        """
        return (
            LRConsts.q0
            + LRConsts.q1 * np.array(v.lcid)
            + LRConsts.q2 * np.array(v.dem)
            + LRConsts.q3 * np.array(v.slope)
            + LRConsts.q4 * np.array(v.alt_diff)
            + LRConsts.q5 * np.array(dists)
        )

    def reset(self) -> None:
        self.active = np.zeros(self.env.dem.shape)
        self.active[self.start.y, self.start.x] = 1

        self.distance = np.full(self.env.dem.shape, np.inf)
        self.distance[self.start.y, self.start.x] = 0

        self.times = np.full(self.env.dem.shape, np.inf)
        self.times[self.start.y, self.start.x] = 0

    def steps(self, num_steps: int, max_dist: float) -> None:
        pbar = tqdm(range(num_steps))
        for i in pbar:
            for a in np.argwhere(self.active > 0):
                y, x = a
                self.active[y, x] = -1

                time = self.times[y, x]
                dist = self.distance[y, x]

                vicinity = self.env.step(Coord(x=x, y=y))

                # Euclidean distances
                dists = self.env.scale * VICINITY_DISTS

                # Calculate time to cross each neighbor
                times = self.time_to_cross(vicinity, dists)

                # Indexes of the cells
                xi, yi = VICINITY_INDICES[0, :] + x, VICINITY_INDICES[1, :] + y

                # Update times and distances based on minimum
                self.times[yi, xi] = np.min([self.times[yi, xi], time + times], axis=0)
                self.distance[yi, xi] = np.min(
                    [self.distance[yi, xi], dist + dists], axis=0
                )

                # Mark these cells as active if they haven't been visited already
                mask = np.where(self.active[yi, xi] == 0)
                self.active[yi[mask], xi[mask]] = 1

            if np.any(self.distance[np.where(np.isfinite(self.distance))] > max_dist):
                logger.debug(
                    f"Max. distance above threshold ({max_dist}m). Stopping simulation"
                )
                return

            pbar.set_description(
                f"Max dist: "
                f"{np.max(self.distance[np.where(np.isfinite(self.distance))]):7.1f}m |"
            )

        logger.debug(
            f"Max. steps ({num_steps}) reached with "
            f"{self.distance[np.where(np.isfinite(self.distance))]=}m. "
            f"Exiting simulation"
        )

    def plot(
        self, ax: matplotlib.pyplot.Axes, *args, **kwargs
    ) -> matplotlib.contour.QuadContourSet:
        z = np.copy(self.times)
        z[np.isinf(z)] = np.nan

        x, y = np.meshgrid(
            np.arange(
                self.env.dem.bounds.left, self.env.dem.bounds.right, self.env.scale
            ),
            np.arange(
                self.env.dem.bounds.bottom, self.env.dem.bounds.top, self.env.scale
            ),
        )
        return ax.contourf(x, y, z, *args, **kwargs)


if __name__ == "__main__":
    logger.debug("Starting LR_Sim")
    sim = LR_Sim()
    sim.steps(800, 2000)

    fig, ax = plt.subplots()

    sim.plot(ax)

    ax.set_xlim([195000, 200000])
    ax.set_ylim([620000, 627500])
    plt.show()

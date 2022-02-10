from typing import Tuple

import numpy as np
import pydantic
import skimage as ski
from Coord import Coord
from Vicinity import Vicinity

from jsim.Environment import Environment


class FourDEnv(Environment):
    def __init__(self, slope: np.ndarray, psim):
        self.psim = psim

        self.slope = slope
        self.edges = ski.feature.canny(self.slope, sigma=1).astype(int)

    @pydantic.validate_arguments
    def get_vicinity(self, coord: Coord) -> Vicinity:
        vicinity = np.zeros((3, 3))
        # TODO check to see if we're at the edge
        vicinity = self.edges[coord.y - 1 : coord.y + 2, coord.x - 1 : coord.x + 2]
        vicinity = np.flipud(
            vicinity
        )  # VERY important. Since the LOWER y coord is the first index above, it
        # flips the image in the y-axis. This doesn't matter for x as we're going
        # left to right
        vicinity = vicinity.reshape((9,))

        return Vicinity(vicinity=list(vicinity))

    def reset(self, agent_p: Coord) -> Vicinity:
        return self.get_vicinity(agent_p)

    def step(self, pa: Coord) -> Tuple[Vicinity, float]:
        return self.get_vicinity(pa), 0

import copy
from typing import List, Tuple, Union

import numpy as np
import rasterio as rs
from Behaviour import BehaviourVector
from Coord import Coord
from Direction import Direction
from FourDAgent import FourDAgent
from FourDEnv import FourDEnv
from loguru import logger
from Vicinity import Vicinity

from jsim.Simulation import Simulation


class FourDSim(Simulation):
    agent: FourDAgent
    env: FourDEnv

    agent_a: Direction
    agent_s: Coord
    vicinity: Vicinity

    data_store: dict[str, Union[List[Coord], Tuple[float, float, float, float]]]

    def __init__(self, initial_pos: Coord, bvecs: List[BehaviourVector] = None):
        self.env = FourDEnv(self._load_slope(), psim=self)

        if bvecs is None:
            self.bvecs = iter(self._generate_bvectors())
        else:
            self.bvecs = iter(bvecs)
        self.initial_pos = initial_pos
        self.agent = FourDAgent(
            bvec=next(self.bvecs),
            pos=copy.deepcopy(self.initial_pos),
            psim=self,
            penv=self.env,
        )

        self.long_term_ds = {}

        self.reset()

    def _load_slope(self) -> np.ndarray:
        dataset_slope = rs.open("./5m_arran_b_merged_slope.tif")

        slope = dataset_slope.read(1)
        slope[slope == -9999.0] = 0
        slope = np.deg2rad(slope)

        return slope

    def _generate_bvectors(self) -> List[BehaviourVector]:
        x = np.arange(0, 1.1, 0.1)
        mesh = np.meshgrid(x, x, x, x)
        vec = np.vstack([f.flatten() for f in mesh])
        vec = vec[:, np.sum(vec, axis=0) == 1.0]
        vec[[0, 1]] = vec[[1, 0]]  # prettier graphs

        bvecs: List[BehaviourVector] = [
            BehaviourVector(rw=f[0], lf=f[1], st=f[2], sp=f[3]) for f in vec.T
        ]

        return bvecs

    def reset(self) -> None:
        self.data_store = {"coords": [], "bvec": None}
        self.vicinity = self.env.reset(copy.deepcopy(self.initial_pos))
        self.agent_a, self.agent_s = self.agent.reset(
            copy.deepcopy(self.initial_pos), self.vicinity
        )

    def trials(self, max_steps_per_trial: int = 300) -> None:
        i = -1
        while True:
            if i % 5 == 0:
                logger.debug(f"Iteration {i}")
            try:
                self.steps(max_steps_per_trial)
            except IndexError:
                pass

            self.long_term_ds[(i := i + 1)] = copy.copy(self.data_store)

            try:
                self.agent.bvec = next(self.bvecs)
            except StopIteration:
                break

    def steps(self, num_steps: int) -> None:
        self.reset()

        self.data_store["bvec"] = self.agent.bvec.tolist()

        for _ in range(num_steps):
            vicinity, _ = self.env.step(self.agent_s)

            self.collect_data(self.agent_s)

            agent_a = self.agent.step(vicinity)

            agent_s = self.agent.update(agent_a)

            if agent_s.x <= 0 or agent_s.y <= 0:
                raise IndexError(f"Out of bounds with {agent_s} <= 0")
            if (
                agent_s.x >= self.env.edges.shape[1] - 1
                or agent_s.y >= self.env.edges.shape[0] - 1
            ):
                raise IndexError(
                    f"Out of bounds with {agent_s} >= \
                    {[f-1 for f in self.env.edges.shape]}"
                )

            self.agent_a = agent_a
            self.agent_s = agent_s
            self.vicinity = vicinity

    def collect_data(self, ps: Coord) -> None:
        self.data_store["coords"].append(copy.deepcopy(ps))


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    logger.debug("Starting")
    sim = FourDSim(
        Coord(x=1900, y=2000), bvecs=[BehaviourVector.fromlist((0.2, 0.3, 0.3, 0.2))]
    )
    logger.debug("Done")
    sim.steps(800)

    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={"aspect": 1})
    x, y = np.array(
        [
            [f.x for f in sim.data_store["coords"]],
            [f.y for f in sim.data_store["coords"]],
        ]
    )
    max_x, max_y = np.max(x), np.max(y)
    min_x, min_y = np.min(x), np.min(y)
    ax.imshow(sim.env.edges, cmap="gray", origin="lower")
    ax.set_ylim([min_y - 10, 10 + max_y])
    ax.set_xlim([min_x - 10, 10 + max_x])
    ax.plot(x, y)
    plt.show()

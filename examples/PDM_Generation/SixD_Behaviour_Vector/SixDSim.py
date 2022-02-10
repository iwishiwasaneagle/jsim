import copy
from typing import List, Tuple, Union

import numpy as np
from Behaviour import BehaviourVector
from Coord import Coord
from Direction import Direction
from loguru import logger
from SixDAgent import SixDAgent
from SixDEnv import SixDEnv
from Vicinity import Vicinity

from jsim.Simulation import Simulation


class SixDSim(Simulation):
    agent: SixDAgent
    env: SixDEnv

    agent_a: Direction
    agent_s: Coord
    vicinity: Tuple[Vicinity, Vicinity]

    data_store: dict[str, Union[List[Coord], Tuple[float, float, float, float]]]

    def __init__(self, initial_pos: Coord, bvecs: List[BehaviourVector] = None):
        self.env = SixDEnv("./5m_arran_b_merged_slope.tif", psim=self)

        if bvecs is None:
            self.bvecs = iter(self._generate_bvectors())
        else:
            self.bvecs = iter(bvecs)
        self.initial_pos = initial_pos
        self.agent = SixDAgent(
            bvec=next(self.bvecs),
            pos=copy.deepcopy(self.initial_pos),
            psim=self,
            penv=self.env,
        )

        self.long_term_ds = {}

        self.reset()

    def _generate_bvectors(self) -> List[BehaviourVector]:
        step = 0.2
        it = np.arange(0, 1 + step, step)
        vecs = np.meshgrid(*(it,) * 6)
        vecs = np.vstack([f.flatten() for f in vecs])
        vecs = vecs[:, np.sum(vecs, axis=0) == 1]

        bvecs: List[BehaviourVector] = [
            BehaviourVector(rw=f[0], lf=f[1], st=f[2], sp=f[3], bt=f[4], ve=f[5])
            for f in vecs.T
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
    import rasterio.plot as rioplot
    import rasterio.transform as riotrans

    logger.debug("Starting")
    sim = SixDSim(
        Coord(x=1900, y=2000),
        bvecs=[BehaviourVector.fromlist((0.2, 0.2, 0.0, 0.0, 0.0, 0.6))],
    )
    logger.debug("Done")
    sim.steps(800)

    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={"aspect": 1})
    x, y = riotrans.xy(
        sim.env.edges.profile["transform"],
        [f.x for f in sim.data_store["coords"]],
        [f.y for f in sim.data_store["coords"]],
    )

    max_x, max_y = np.max(x), np.max(y)
    min_x, min_y = np.min(x), np.min(y)

    hidden_img = plt.imshow(
        sim.env.slope.read(1),
        extent=[sim.env.slope.bounds[i] for i in [0, 2, 1, 3]],
        cmap="jet",
    )
    rioplot.show(sim.env.slope, cmap="jet", ax=ax)
    ax.set_ylim([min_y - 50, 50 + max_y])
    ax.set_xlim([min_x - 50, 50 + max_x])
    ax.plot(x, y, "r")
    fig.colorbar(hidden_img)
    plt.show()

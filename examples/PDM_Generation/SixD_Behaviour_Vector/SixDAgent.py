import copy
from typing import Tuple

import numpy as np
import pydantic
from Behaviour import Behaviour, BehaviourEnum, BehaviourVector, SixDBehaviours
from Coord import Coord
from Direction import Direction
from Vicinity import Vicinity

from jsim.Agent import Agent


class SixDAgent(Agent):
    direction: Direction

    def __init__(self, bvec: BehaviourVector, pos: Coord, psim, penv):
        self.psim = psim
        self.penv = penv

        self.bvecs = SixDBehaviours(  # bt and ve are not vector based.
            rw=Behaviour(p=list(np.ones(9) / 9)),
            lf=Behaviour(
                p=[1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0]
            ),  # if on a linear feature
            sp=Behaviour(p=[0, 0, 0, 0, 1, 0, 0, 0, 0]),
        )
        self.bvec = bvec

        self.state = copy.deepcopy(pos)

    #    @pydantic.validate_arguments
    def policy(self, pnext_s: Tuple[Vicinity, Vicinity]) -> Direction:
        edges, slopes = pnext_s
        choice = np.random.choice(np.arange(0, len(self.bvec)), p=self.bvec.tolist())

        if choice == BehaviourEnum.st:
            new_direction = self.direction

        elif choice == BehaviourEnum.lf:
            if np.sum(edges.vicinity) == 0:
                new_direction = np.random.choice(
                    np.arange(0, len(self.bvecs.rw)), p=self.bvecs.rw.p
                )
            else:
                new_direction = np.random.choice(
                    np.where(np.array(edges.vicinity) > 0)[0]
                )  # + np.random.randint(-1, 1)
                new_direction = new_direction % 9

        elif choice == BehaviourEnum.bt:
            if self.direction == Direction.sp:
                new_direction = np.random.choice(
                    np.arange(0, len(self.bvecs.rw)), p=self.bvecs.rw.p
                )
            else:
                dirs = np.array([0, 1, 2, 5, 8, 7, 6, 3])  # circular directions
                new_direction = (np.where(dirs == int(self.direction))[0] - 4) % 8

        elif choice == BehaviourEnum.ve:
            new_direction = np.where(slopes.vicinity == np.max(slopes.vicinity))[0][0]

        else:
            new_direction = np.random.choice(
                np.arange(0, len(self.bvecs[choice])), p=self.bvecs[choice].p
            )

        return Direction(new_direction)

    def step(self, pnext_s: Tuple[Vicinity, Vicinity]) -> Direction:
        return self.policy(pnext_s)

    @pydantic.validate_arguments
    def update(self, pa: Direction) -> Coord:
        xy = Direction.dir_to_coord(pa)
        if self.state.x == 0:
            print(self.state)
        self.state.x += xy.x
        self.state.y += xy.y

        self.direction = pa
        return self.state

    @pydantic.validate_arguments
    def reset(
        self,
        ps: Coord,
        vicinities: Tuple[Vicinity, Vicinity],
        bvec: BehaviourVector = None,
    ) -> Tuple[Direction, Coord]:
        self.state = copy.deepcopy(ps)
        if bvec is not None:
            self._bvec = copy.copy(bvec)
        self.direction = Direction(np.random.choice([0, 1, 2, 3, 5, 6, 7, 8]))

        return self.policy(vicinities), self.state


if __name__ == "__main__":
    # Test the LF
    agent = SixDAgent(
        BehaviourVector.fromlist(tuple(np.ones(6) / 6)),
        Coord(x=1900, y=2000),
        None,
        None,
    )
    for _ in range(500):
        agent.direction = Direction(int(np.random.randint(0, 9)))
        agent.step((Vicinity(vicinity=list(np.random.randint(0, 2, size=(9,)))),) * 2)

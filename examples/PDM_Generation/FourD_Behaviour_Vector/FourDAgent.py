import copy
from typing import Tuple

import numpy as np
import pydantic
from Behaviour import Behaviour, BehaviourEnum, BehaviourVector, FourDBehaviours
from Coord import Coord
from Direction import Direction
from Vicinity import Vicinity

from jsim.Agent import Agent


class FourDAgent(Agent):
    direction: Direction

    def __init__(self, bvec: BehaviourVector, pos: Coord, psim, penv):
        self.psim = psim
        self.penv = penv

        self._behavior = FourDBehaviours(
            rw=Behaviour(p=list(np.ones(9) / 9)),
            lf=Behaviour(
                p=[1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0]
            ),  # if on a linear feature
            st=Behaviour(p=[0, 1, 0, 0, 0, 0, 0, 0, 0]),
            sp=Behaviour(p=[0, 0, 0, 0, 1, 0, 0, 0, 0]),
        )
        self.bvec = bvec

        self.state = pos

    @pydantic.validate_arguments
    def policy(self, pnext_s: Vicinity) -> Direction:
        choice = np.random.choice(np.arange(0, len(self.bvec)), p=self.bvec.tolist())

        if choice == BehaviourEnum.st:
            new_direction = self.direction
        elif choice == BehaviourEnum.lf:
            if np.sum(pnext_s.vicinity) == 0:
                new_direction = np.random.choice(
                    np.arange(0, len(self._behavior.rw)), p=self._behavior.rw.p
                )
            else:
                new_direction = np.random.choice(
                    np.where(np.array(pnext_s.vicinity) > 0)[0]
                )  # + np.random.randint(-1, 1)
                new_direction = new_direction % 9
        else:
            new_direction = np.random.choice(
                np.arange(0, len(self._behavior[choice])), p=self._behavior[choice].p
            )

        return Direction(new_direction)

    def step(self, pnext_s: Vicinity) -> Direction:
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
        self, ps: Coord, vicinity: Vicinity, bvec: BehaviourVector = None
    ) -> Tuple[Direction, Coord]:
        self.state = copy.deepcopy(ps)
        if bvec is not None:
            self._bvec = copy.copy(bvec)
        self.direction = Direction(np.random.choice([0, 1, 2, 3, 5, 6, 7, 8]))

        return self.policy(vicinity), self.state


if __name__ == "__main__":
    # Test the LF
    agent = FourDAgent(
        BehaviourVector.fromlist((0.0, 1.0, 0.0, 0.0)),
        Coord(x=2000, y=2000),
        None,
        None,
    )
    fake_vicinity = Vicinity(vicinity=[1, 1, 1, 0, 0, 0, 0, 0, 0])
    assert agent.step(fake_vicinity) in [Direction.tl, Direction.t, Direction.tr]

    agent.direction = Direction.t
    assert agent.step(fake_vicinity) in [Direction.tl, Direction.t, Direction.tr]

    print(agent.step(Vicinity(vicinity=[0, 0, 0, 0, 0, 0, 0, 0, 0])))

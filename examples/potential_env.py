from typing import Tuple

import matplotlib.pyplot as plt
from tqdm.std import tqdm

from jsim.Agent import Agent
from jsim.Environment import Environment
from jsim.Meta import Action, Sensation
from jsim.Simulation import Simulation


class Force(Action):
    def __init__(self, x=0.0, y=0.0) -> None:
        super().__init__()

        self.x = x
        self.y = y


class XYSensation(Sensation):
    def __init__(self, x=0, y=0) -> None:
        super().__init__()

        self.x = x
        self.y = y


class Position(XYSensation):
    pass


class Velocity(XYSensation):
    pass


class Acceleration(XYSensation):
    pass


class State(Sensation):
    def __init__(self, position=None, velocity=None, acceleration=None) -> None:
        super().__init__()
        if position is None:
            position = Position()

        if velocity is None:
            velocity = Velocity()

        if acceleration is None:
            acceleration = Acceleration()

        self.pos = position
        self.vel = velocity
        self.acc = acceleration


class PotentialAgent(Agent):
    def __init__(self) -> None:
        super().__init__()

        self.start_trial(State())

    def start_trial(self, ps: State) -> Action:
        self.state = ps

        return self.policy(ps)

    def step(
        self, ps: Sensation, pa: Action, pnext_s: Sensation, reward: float
    ) -> Action:

        return self.policy(ps)

    def policy(self, pnext_s: Sensation) -> Action:
        """
        Simple potential function following to the minima.

            $$fx = d/dx [ (x-20)^2 + (y-20)^2 ] = 2(x-20)$$
            $$fy = d/dy [ (x-20)^2 + (y-20)^2 ] = 2(y-20)$$
        """

        fx = -2 * (pnext_s.pos.x - 20)  # minus to make it go towards the centre
        fy = -2 * (pnext_s.pos.y - 20)

        return Force(fx, fy)


class PotentialEnv(Environment):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def start_trial(self) -> State:
        return State(position=Position(15), velocity=Velocity(-3, -3))

    def step(self, pa: Force, ps: State) -> Tuple[State, float]:
        p, v, a = ps.pos, ps.vel, ps.acc
        fx, fy = pa.x, pa.y

        a.x = fx * 0.1 - 0.4 * v.x
        a.y = fy * 0.1 - 0.4 * v.y

        v.x += a.x * self.psim.dt
        v.y += a.y * self.psim.dt

        p.x += v.x * self.psim.dt
        p.y += v.y * self.psim.dt

        return State(p, v, a), 0


class MySim(Simulation):
    def __init__(self, dt=0.1) -> None:
        super().__init__(PotentialAgent, PotentialEnv, dt=dt)
        self.pos_arr = []

    def collect_data(self, ps: State, pa: Force, pnext_s: State, reward: float) -> None:

        self.pos_arr.append((ps.pos.x, ps.pos.y))

    def steps(self, num_steps: int) -> None:
        for _ in tqdm(range(num_steps), leave=False):
            next_s, reward = self.env.step(self.action, self.sensation)

            self.collect_data(self.sensation, self.action, next_s, reward)

            next_a = self.agent.step(self.sensation, self.action, next_s, reward)

            if next_s != 0:
                self.action = next_a
                self.sensation = next_s
            else:
                self.start_trial()
                break


if __name__ == "__main__":
    mysim = MySim()

    mysim.steps(1000)

    pos_x = [p[0] for p in mysim.pos_arr]
    pos_y = [p[1] for p in mysim.pos_arr]
    t = [mysim.dt * i for i in range(len(pos_x))]

    fig = plt.figure()

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.plot(pos_x, pos_y)

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.plot(t, pos_x)
    ax2.plot(t, pos_y)

    plt.show()

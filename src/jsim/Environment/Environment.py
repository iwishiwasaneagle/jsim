"""
The environment defines the problem to be solved. It determines the dynamics of the
environment, the rewards, and the trial terminations.
"""
from abc import ABC, abstractmethod
from typing import Tuple

from jsim.Meta import Action, State
from jsim.Simulation import Simulation


class Environment(ABC):
    """
    Base class of all environments. Specific environments are instances of subclassed
    derived from here.
    """

    @abstractmethod
    def __init__(self, psim: Simulation = None) -> None:
        """
        Typically provided by the user for their specialized environment. If the
        environment changes in any way with experience, then this function should
        reset it to its original, naive condition.

        Called once when the simulation is first assembled and inited.

        The corresponding agent is not available at the time Environment is created.
        """
        self.psim = psim
        pass

    @abstractmethod
    def reset(self) -> State:  # pragma: no cover
        """
        This function must be provided by the user for their specialized environment.
        Called at the beginning of a new trial and should perform any needed
        initialization of the environment to prepare for a new trial.

        :return: First state of the trial
        :rtype: State
        """
        pass

    @abstractmethod
    def step(self, pa: Action) -> Tuple[State, float]:  # pragma: no cover
        """
        Must be provided by the user for their specialized environment. Called once
        every simulation step and causes the environment to undergo a transition
        from its current state to a next state dependent on the action taken by `pa`.

        Note:
            If the environment transitions into a terminal state, the returned state
            will have a special value of 0

        :param pa: The action to be taken by the :py:class:`Agent`
        :type pa: Action
        :return:
            - state - The next state due to action `pa`
            - reward - The payoff for the state transition due to action `pa`
        :rtype: Tuple[State, float]
        """
        pass

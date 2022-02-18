"""
The base object of the interface. The Simulation handles the interaction between the
agent and the environment.

A simulation class is created by deriving from `Simulation` and providing the
implementation to `collect_data()`.
"""
from abc import ABC, abstractmethod

from loguru import logger
from tqdm.autonotebook import tqdm

from jsim.Meta import Action, State


class Simulation(ABC):
    """
    Basic class of all simulations. An instance of the simulation is associated with an
    agent and an environment instances at the moment of creation.
    """

    def __init__(self) -> None:
        """
        Initializes the simulation instance, the agent, and the environment.
        `reset` is called after initializing the aforementioned classes.

        Example:

        .. code-block::

            self.env: Environment = pe(self)
            self.agent: Agent = pa(self, self.env)
        """
        self.reset()

    @abstractmethod
    def reset(self) -> None:  # pragma: no cover
        """
        Forces the beginning of a new trial. Calls `self.pa.reset()` and
        `self.pe.reset()` to get the first action and state respectively.

        Example:

        .. code-block:: python

            self.state = self.env.reset()
            self.action = self.agent.reset(self.state)
        """
        pass

    @abstractmethod
    def steps(self, num_steps: int) -> None:  # pragma: no cover
        """
        Runs the simulation for `num_steps` steps, starting from whatever state the
        environment is in. If the terminal state is reached, it should immediately
        prepare for the next trail by callied `reset`. Switching from terminal
        state to a new state does not count as a step.

        :param num_steps: Number of steps per trial
        :type num_steps: int

        Example:

        .. code-block:: python

            for _ in range(num_steps):
                # Step through environment
                next_s, r = self.env.step(self.action)

                # Store data as defined in self.collect_data (default does nothing)
                self.collect_data(self.state, self.action, next_state, r)

                # Step the agent
                next_a = self.agent.step(self.state, self.action, next_s, r)

                # Check if terminal constraint has been met
                if next_state != 0:
                    self.action = next_a
                    self.state = next_s
                else:
                    print(
                        "Terminal state was returned from self.env.step, \
                            exiting current trial."
                    )
                    self.reset()
                    break
        """
        pass

    def trials(self, num_trials: int, max_steps_per_trial: int) -> None:
        """
        Runs the simulation for `num_trials`, starting from whatever state the
        environment is in. Each trial should be no longer than `max_steps_per_trial`.

        :param num_trials: Maximum number of trials
        :type num_trials: int
        :param max_steps_per_trial: Maximum number of steps per trial
        :type max_steps_per_trial: int
        """
        logger.info(
            f"Running {num_trials} trials with a maximum steps per trial \
                of {max_steps_per_trial}"
        )
        for _ in tqdm(range(num_trials)):
            self.steps(max_steps_per_trial)

    def collect_data(
        self, ps: State, pa: Action, pnext_s: State, reward: float
    ) -> None:  # pragma: no cover
        """
        This function is called once on each step of the simulation. The default method
        does nothing. This is where the user can gain access to the simulation's
        behaviour.

        :param ps: Previous state, off of which the action was decided
        :type ps: State
        :param pa: The action taken
        :type pa: Action
        :param pnext_s: The state from the environment as a result of `pa`
        :type pnext_s: State
        :param reward: The reward gained by taking action `pa`
        :type reward: float
        """
        pass

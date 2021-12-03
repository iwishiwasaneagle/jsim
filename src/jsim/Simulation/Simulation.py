"""
The base object of the interface. The Simulation handles the interaction between the
agent and the environment.

A simulation class is created by deriving from `Simulation` and providing the
implementation to `collect_data()`.
"""
from abc import ABC

from loguru import logger
from tqdm import tqdm

from jsim.Agent import Agent
from jsim.Environment import Environment
from jsim.Meta import Action, Sensation


class Simulation(ABC):
    """
    Basic class of all simulations. An instance of the simulation is associated with an
    agent and an environment instances at the moment of creation.
    """

    def __init__(self, pa: Agent, pe: Environment, dt=0.1) -> None:
        """
        Initializes the simulation instance, the agent, and the environment.
        `reset` is called after initializing the aforementioned classes.

        :param pa: The agent to initialize with the simulation
        :type pa: Agent
        :param pe: The environment to initialize with the simulation
        :type pe: Environment
        """
        self.dt = dt

        self.env: Environment = pe(psim=self)
        self.sensation: Sensation = None
        self.agent: Agent = pa()
        self.action: Action = None

        self.reset()

    def reset(self) -> None:
        """
        Forces the beginning of a new trial. Calls `self.pa.reset()` and
        `self.pe.reset()` to get the first action and sensation respectively.
        """
        self.sensation = self.env.reset()
        self.action = self.agent.reset(self.sensation)

    def steps(self, num_steps: int) -> None:
        """
        Runs the simulation for `num_steps` steps, starting from whatever state the
        environment is in. If the terminal state is reached, it should immediately
        prepare for the next trail by callied `reset`. Switching from terminal
        state to a new state does not count as a step.

        :param num_steps: Number of steps per trial
        :type num_steps: int
        """
        for _ in tqdm(range(num_steps), leave=False):
            # Step through environment
            next_sensation, reward = self.env.step(self.action)

            # Store data as defined in self.collect_data (default does nothing)
            self.collect_data(self.sensation, self.action, next_sensation, reward)

            # Step the agent
            next_action = self.agent.step(
                self.sensation, self.action, next_sensation, reward
            )

            # Check if terminal constraint has been met
            if next_sensation != 0:
                self.action = next_action
                self.sensation = next_sensation
            else:
                logger.info(
                    "Terminal state was returned from self.env.step, \
                        exiting current trial."
                )
                self.reset()
                break

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
        self, ps: Sensation, pa: Action, pnext_s: Sensation, reward: float
    ) -> None:
        """
        This function is called once on each step of the simulation. The default method
        does nothing. This is where the user can gain access to the simulation's
        behaviour.

        :param ps: Previous sensation, off of which the action was decided
        :type ps: Sensation
        :param pa: The action taken
        :type pa: Action
        :param pnext_s: The sensation from the environment as a result of `pa`
        :type pnext_s: Sensation
        :param reward: The reward gained by taking action `pa`
        :type reward: float
        """
        pass

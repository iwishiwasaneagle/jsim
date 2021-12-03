"""
The agent entity moves around and interacts with the environment. From the environment,
it receives states and selects actions. The agent may or may not learn, may or may
not build a model of the environment (i.e SLAM), etc.
"""

from abc import ABC, abstractmethod

from jsim.Meta import Action, State


class Agent(ABC):
    """
    Agent class to be placed within the simulation.
    """

    @abstractmethod
    def __init__(self) -> None:
        """
        Extended by the user for their specialised use case. Called once at the
        instantiation of the simulation.

        The agent can consult with the environment or simulation as needed. Both are
        guaranteed to be existant and inited by the time the Agent is created.
        """
        pass

    @abstractmethod
    def reset(self, ps: State) -> Action:
        """
        Extended by the user for their specialised use case. Called at the beginning
        of each new trial. Should perform any needed initialization of the agent to
        prepare it for beginning a new trial.

        :param ps: The first state of the trial.
        :type ps: state
        :return: The first action of the agent in the new trial, in response to `ps`
        :rtype: Action
        """
        pass

    @abstractmethod
    def step(self, ps: State, pa: Action, pnext_s: State, reward: float) -> Action:
        """
        Must be provided by the user and will be called at each step of the
        simulation. This is the place where the learning should take place.

        :param ps: State used to decide on previous step
        :type ps: State
        :param pa: Action taken due to decision in previous step
        :type pa: Action
        :param pnext_s: State to decide the action on
        :type pnext_s: State
        :param reward: The reward gained from the previous action
        :type reward: float
        :return: The next action to be taken
        :rtype: Action
        """
        pass

    def learn(self) -> None:
        """
        The area for the agent to learn. This is called by the simulation at the end of
        every step/trial/whenever is suitable. Inputs are highly specific to the users
        use case.
        """
        pass

    @abstractmethod
    def policy(self, pnext_s: State) -> Action:
        """
        Must be provided by the user. This encodes the agents response to a given
        state.

        :param pnext_s: The currently sensed State (i.e. the current state)
        :type pnext_s: State
        :return: The action to take given the state
        :rtype: Action
        """
        pass

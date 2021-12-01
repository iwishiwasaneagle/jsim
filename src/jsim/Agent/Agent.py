"""
The agent entity moves around and interacts with the environment. From the environment,
it receives sensations and selects actions. The agent may or may not learn, may or may
not build a model of the environment (i.e SLAM), etc.
"""

from jsim.Meta import Action, Sensation


class Agent:
    """
    Agent class to be placed within the simulation.
    """

    def __init__(self) -> None:
        """
        Extended by the user for their specialised use case. Called once at the
        instantiation of the simulation.

        The agent can consult with the environment or simulation as needed. Both are
        guaranteed to be existant and inited by the time the Agent is created.
        """
        raise NotImplementedError

    def start_trial(self, ps: Sensation) -> Action:
        """
        Extended by the user for their specialised use case. Called at the beginning
        of each new trial. Should perform any needed initialization of the agent to
        prepare it for beginning a new trial.

        :param ps: The first sensation of the trial.
        :type ps: Sensation
        :return: The first action of the agent in the new trial, in response to `ps`
        :rtype: Action
        """
        raise NotImplementedError

    def step(
        self, ps: Sensation, pa: Action, pnext_s: Sensation, reward: float
    ) -> Action:
        """Must be provided by the user and will be called at each step of the
        simulation. This is the place where the learning should take place.

        :param ps: Sensation used to decide on previous step
        :type ps: Sensation
        :param pa: Action taken due to decision in previous step
        :type pa: Action
        :param pnext_s: Sensation to decide the action on
        :type pnext_s: Sensation
        :param reward: The reward gained from the previous action
        :type reward: float
        :return: The next action to be taken
        :rtype: Action
        """
        raise NotImplementedError

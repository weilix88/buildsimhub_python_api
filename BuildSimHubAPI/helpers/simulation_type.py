class SimulationType(object):

    def __init__(self):
        self._type = "regular"
        self._agent = 1

    @property
    def type(self):
        return self._type

    @property
    def agent(self):
        return self._agent

    def set_regular(self):
        self._type = "regular"

    def increase_agents(self):
        if self._agent == 1:
            self._agent = 1
            return self._agent
        elif self._agent == 2:
            self._agent = 4
            return self._agent
        else:
            return self._agent

    def reset_agent(self):
        self._agent = 1
        return self._agent

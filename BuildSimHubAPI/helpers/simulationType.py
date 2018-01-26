class SimulationType():

    def __init__(self):
        self._regular = "regular"
        self._fast = "fast"
        self._agent = 2

    @property
    def regular(self):
        return self._regular

    @property
    def fast(self):
        return self._fast

    @property
    def agent(self):
        return self._agent

    def increaseAgents(self):
        if(self._agent < 6):
            self._agent += 2
            return self._agent
        elif(self._agent == 6):
            self._agent = 12
            return self._agent
        else:
            return self._agent

    def resetAgent(self):
        self._agent = 2
        return self._agent
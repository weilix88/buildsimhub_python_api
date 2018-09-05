from .model_action import ModelAction


class CoolingChillerCOP(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'cooling_chillers')
        self._measure_name = 'ChillerCOP'
        self._lower_limit = 0

    def _unit_convert_ratio(self):
        return 1

from .model_action import ModelAction


class CoolingCoilCOP(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'cooling_coils')
        self._measure_name = 'CoolingCoilCOP'
        self._lower_limit = 0

    def _unit_convert_ratio(self):
        return 1

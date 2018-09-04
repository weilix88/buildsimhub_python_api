from .model_action import ModelAction


class CoolingCOP(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'cooling_all_equip')
        self._measure_name = 'CoolingCOP'
        self._lower_limit = 0

    def _unit_convert_ratio(self):
        return 1

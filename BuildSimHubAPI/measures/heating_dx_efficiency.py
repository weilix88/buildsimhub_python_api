from .model_action import ModelAction


class HeatingDXEfficiency(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'heating_dx_equip')
        self._measure_name = 'HeatCOP'
        self._lower_limit = 0

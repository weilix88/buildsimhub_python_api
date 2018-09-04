from .model_action import ModelAction


class HeatingEfficiency(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'heating_all_equip')
        self._measure_name = 'HeatingEff'
        self._lower_limit = 0
        self._upper_limit = 1

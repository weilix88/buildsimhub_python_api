from .model_action import ModelAction


class WaterHeaterEfficiency(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'water_heater_equipment')
        self._measure_name = 'WaterHeater'
        self._lower_limit = 0
        self._upper_limit = 1

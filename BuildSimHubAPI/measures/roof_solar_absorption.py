from .model_action import ModelAction


class RoofSolarAbsorption(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'roof_absorption')
        self._measure_name = 'Roof_Absorption'
        self._lower_limit = 0
        self._upper_limit = 1

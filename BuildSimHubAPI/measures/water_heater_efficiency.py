from .model_action import ModelAction


class WaterHeaterEfficiency(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'water_heater_equipment')
        self._measure_name = 'WaterHeater'
        self._lower_limit = 0
        self._upper_limit = 1
        self._measure_help = '''
        measure name: WaterHeater
        Unit: ip or si
        Minimum: 0.1
        Maximum: NA
        Type: numeric

        This measure will update the water heater efficiency - works on class:
        WaterHeater:Mixed, WaterHeater:Stratified
        '''
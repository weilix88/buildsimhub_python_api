from .model_action import ModelAction


class WaterUseReduction(ModelAction):
    def __init__(self, unit="si"):
        ModelAction.__init__(self, 'water_use_reduction', unit)
        self._measure_name = 'Water_Use'
        self._lower_limit = 0
        self._upper_limit = 1
        self._measure_help = '''
        measure name: Water_Use
        Unit: Not required
        Minimum: 0.1
        Maximum: 1
        Type: numeric

        This measure will update the water usage of water equipment (WaterUse:Equipment) by percentage
        The percentage is the remaining percentage - e.g. if user input is 0.8,
        It means the water usage will be 80% of its original level.
        '''
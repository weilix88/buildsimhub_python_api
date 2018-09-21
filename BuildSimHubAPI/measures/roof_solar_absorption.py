from .model_action import ModelAction


class RoofSolarAbsorption(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'roof_absorption')
        self._measure_name = 'Roof_Absorption'
        self._lower_limit = 0
        self._upper_limit = 1
        self._measure_help = '''
        measure name: Roof_Absorption
        Unit: Not required
        Minimum: 0.1
        Maximum: 1
        Type: numeric

        This measure will update the Solar Absorptance of the out most layer of the roof construction
        '''
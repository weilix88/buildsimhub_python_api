from .model_action import ModelAction


class HeatingEfficiency(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'heating_all_equip')
        self._measure_name = 'HeatingEff'
        self._lower_limit = 0
        self._upper_limit = 1
        self._measure_help = '''
        measure name: HeatingEff
        Unit: Not required
        Minimum: 0
        Maximum: 1
        Type: numeric

        This measure will update all the thermal efficiency heating equipment, including:
        Coil:Heating:Fuel, Coil:Heating:Gas:MultiStage,
        Boiler:HotWater, Boiler:Steam, HeatPump:WaterToWater:ParameterEstimation:Heating
        '''
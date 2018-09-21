from .model_action import ModelAction


class HeatingDXEfficiency(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'heating_dx_equip')
        self._measure_name = 'HeatCOP'
        self._lower_limit = 0
        self._measure_help = '''
        measure name: HeatCOP
        Unit: not required
        Minimum: 1.1
        Maximum: NA
        Type: numeric

        This measure will update all the COPs of DX heating coils, including:
        Coil:Heating:DX:SingleSpeed, Coil:Heating:DX:MultiSpeed, Coil:Heating:DX:VariableSpeed,
        Coil:Heating:WaterToAirHeatPump:EquationFit, Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit,
        Coil:WaterHeating:AirToWaterHeatPump:Pumped, Coil:WaterHeating:AirToWaterHeatPump:Wrapped,
        HeatPump:WaterToWater:ParameterEstimation:Heating
        '''
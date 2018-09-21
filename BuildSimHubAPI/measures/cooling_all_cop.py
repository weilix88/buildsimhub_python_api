from .model_action import ModelAction


class CoolingCOP(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'cooling_all_equip')
        self._measure_name = 'CoolingCOP'
        self._lower_limit = 0
        self._measure_help = '''
        measure name: CoolingCOP
        Unit: Not required
        Minimum: 0
        Maximum: NA
        Type: numeric

        This measure will update the COP of all cooling equipment include:
        Coil:Cooling:DX:SingleSpeed, Coil:Cooling:DX:TwoSpeed,Coil:Cooling:DX:MultiSpeed, Coil:Cooling:DX:VariableSpeed,
        CoilPerformance:DX:Cooling, Coil:Cooling:WaterToAirHeatPump:EquationFit,
        Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit, Chiller:Electric:EIR,
        Chiller:Electric:ReformulatedEIR, Chiller:Electric, Chiller:ConstantCOP, Chiller:EngineDriven,
        Chiller:CombustionTurbine, HeatPump:WaterToWater:ParameterEstimation:Cooling
        
        For equipment with multiple COPs (e.g., Coil:Cooling:DX:TwoSpeed), this measure only changes the first 
        encountered COP.
        '''

    def _unit_convert_ratio(self):
        return 1

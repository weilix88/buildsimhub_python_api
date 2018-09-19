from .model_action import ModelAction


class CoolingChillerCOP(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'cooling_chillers')
        self._measure_name = 'ChillerCOP'
        self._lower_limit = 0
        self._measure_help = '''
        measure name: ChillerCOP
        Unit: Not required
        Minimum: 0
        Maximum: NA
        Type: numeric

        This measure will update the COP of all chiller equipment include:
        Chiller:Electric:EIR, Chiller:Electric:ReformulatedEIR, Chiller:Electric, Chiller:ConstantCOP, 
        Chiller:EngineDriven, Chiller:CombustionTurbine, HeatPump:WaterToWater:ParameterEstimation:Cooling
        '''

    def _unit_convert_ratio(self):
        return 1

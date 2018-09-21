from .model_action import ModelAction

# The infiltration has default values
# that is determined based on standards (PNNL models)
# These default values will be used for default parametric exploration


class Infiltration(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'infiltration')
        self._default_list = [-1, -2, -3]
        self._measure_name = 'Infiltration'
        self._lower_limit = 0
        self._measure_help = '''
        measure name: Infiltration
        Unit: ip or si
        Minimum: 0
        Maximum: 1
        Type: numeric

        This measure will update the percentage in the 
        ZoneInfiltration:DesignFlowRate
        The percentage is the remaining percentage - e.g. if user input is 0.8,
        It means the infiltration value will be 80% of its original level.
        '''

    def set_datalist(self, datalist):
        ModelAction.set_datalist(self, datalist)

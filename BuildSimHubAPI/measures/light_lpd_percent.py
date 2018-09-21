from .model_action import ModelAction


class LightLPDPercent(ModelAction):
    
    def __init__(self):
        ModelAction.__init__(self, 'lpd_percent')
        self._measure_name = 'LPDPercent'
        self._lower_limit = 0
        self._measure_help = '''
        measure name: LPDPercent
        Unit: Not required
        Minimum: 0.1
        Maximum: NA
        Type: numeric

        This measure will update the power density by percentage in the 
        Lights.
        The percentage is the remaining percentage - e.g. if user input is 0.8,
        It means the equipment power density will be 80% of its original level.
        '''


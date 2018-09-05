from .model_action import ModelAction


class LightLPDPercent(ModelAction):
    
    def __init__(self):
        ModelAction.__init__(self, 'lpd_percent')
        self._measure_name = 'LPDPercent'
        self._lower_limit = 0



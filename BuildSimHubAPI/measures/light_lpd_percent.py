from .model_action import ModelAction


class LightLPDPercent(ModelAction):
    
    def __init__(self):
        ModelAction.__init__(self, 'lpd_percent')
        self._measure_name = 'LPDPercent'
        self._lower_limit = 0
        self._upper_limit = 1

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        ModelAction.set_datalist(self, datalist)


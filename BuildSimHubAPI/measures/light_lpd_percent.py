from .model_action import ModelAction


class LightLPDPercent(ModelAction):
    
    def __init__(self):
        ModelAction.__init__(self, 'lpd_percent')

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        ModelAction.set_datalist(self, datalist)


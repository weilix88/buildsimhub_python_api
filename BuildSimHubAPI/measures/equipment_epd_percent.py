from .model_action import ModelAction


class EquipmentEPDPercent(ModelAction):

    def __init__(self):
        ModelAction.__init__(self, 'epd_percent')
        self._measure_name = 'EPDPercent'
        self._lower_limit = 0
        self._upper_limit = 1

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        ModelAction.set_datalist(self, datalist)


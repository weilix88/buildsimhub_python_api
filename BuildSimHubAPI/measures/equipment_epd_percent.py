from .model_action import ModelAction


class EquipmentEPDPercent(ModelAction):

    def __init__(self):
        ModelAction.__init__(self, 'epd_percent')

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        ModelAction.set_datalist(self, datalist)


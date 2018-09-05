from .model_action import ModelAction


class EquipmentEPDPercent(ModelAction):

    def __init__(self):
        ModelAction.__init__(self, 'epd_percent')
        self._measure_name = 'EPDPercent'
        self._lower_limit = 0


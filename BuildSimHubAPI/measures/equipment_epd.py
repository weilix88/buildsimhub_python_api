from .model_action import ModelAction


class EquipmentEPD(ModelAction):
    # this shows the ip to si conversion rate
    # if unit is 'ip', then multiply this rate.
    # for window it is the U-value
    # convert U-value IP to SI
    # The conversion will change w/m2 to w/ft2 if ip shows
    CONVERSION_RATE = 0.0929

    def __init__(self, unit="si"):
        ModelAction.__init__(self, 'equipment_epd', unit)
        self._measure_name = 'EPD'
        self._lower_limit = 0

    def _unit_convert_ratio(self):
        return EquipmentEPD.CONVERSION_RATE

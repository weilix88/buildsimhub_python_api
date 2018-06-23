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

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        if ModelAction.unit(self) == 'ip':
            for i in range(len(datalist)):
                datalist[i] = datalist[i] / EquipmentEPD.CONVERSION_RATE
        ModelAction.set_datalist(self, datalist)

    def set_data(self, data):
        if ModelAction.unit(self) == 'ip':
            data = data / EquipmentEPD.CONVERSION_RATE
        ModelAction.set_data(self, data)

    def set_min(self, min_val):
        if ModelAction.unit(self) == 'ip':
            min_val = min_val / EquipmentEPD.CONVERSION_RATE
        ModelAction.set_min(self, min_val)

    def set_max(self, max_val):
        if ModelAction.unit(self) == 'ip':
            max_val = max_val / EquipmentEPD.CONVERSION_RATE
        ModelAction.set_max(self, max_val)

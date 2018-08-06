from .model_action import ModelAction


class WindowUValue(ModelAction):
    # this shows the ip to si conversion rate
    # if unit is 'ip', then multiply this rate.
    # for window it is the U-value
    # convert U-value IP to SI
    CONVERSION_RATE = 5.678

    def __init__(self, unit="si", orientation=None):

        if orientation is None:
            ModelAction.__init__(self, 'window_uvalue', unit)
        else:
            orientation = orientation.lower()
            if orientation == 'w':
                ModelAction.__init__(self, 'window_uvalue_w', unit)
            elif orientation == 'e':
                ModelAction.__init__(self, 'window_uvalue_e', unit)
            elif orientation == 's':
                ModelAction.__init__(self, 'window_uvalue_s', unit)
            elif orientation == 'n':
                ModelAction.__init__(self, 'window_uvalue_n', unit)
            else:
                ModelAction.__init__(self, 'window_uvalue', unit)

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        if ModelAction.unit(self) == 'ip':
            for i in range(len(datalist)):
                datalist[i] = datalist[i] * WindowUValue.CONVERSION_RATE
        ModelAction.set_datalist(self, datalist)

    def set_data(self, data):
        if ModelAction.unit(self) == 'ip':
            data = data * WindowUValue.CONVERSION_RATE
        ModelAction.set_data(self, data)

    def set_min(self, min_val):
        if ModelAction.unit(self) == 'ip':
            min_val = min_val * WindowUValue.CONVERSION_RATE
        ModelAction.set_min(self, min_val)

    def set_max(self, max_val):
        if ModelAction.unit(self) == 'ip':
            max_val = max_val * WindowUValue.CONVERSION_RATE
        ModelAction.set_max(self, max_val)

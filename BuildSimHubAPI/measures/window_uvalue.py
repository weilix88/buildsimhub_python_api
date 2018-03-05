from .model_action import ModelAction


class WindowUValue(ModelAction):
    # this shows the ip to si conversion rate
    # if unit is 'ip', then multiply this rate.
    # for window it is the U-value
    # convert U-value IP to SI
    CONVERSION_RATE = 5.678

    def __init__(self, unit="si"):
        ModelAction.__init__(self, 'window_uvalue', unit)

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        if ModelAction.unit(self) == 'ip':
            for i in range(len(datalist)):
                datalist[i] = datalist[i] * WindowUValue.CONVERSION_RATE
        ModelAction.set_datalist(self, datalist)

#########TEST CODE###############
# wp = WindowProperty('ip')
# a = [1.1,2.2,3.3]
# wp.add_uvalue_list(a)
# b = [0.2,0.3,0.4,0.6]
# wp.add_shgc_list(b)
# print(wp.get_num_combination())

from .model_action import ModelAction


class WindowSHGC(ModelAction):

    def __init__(self):
        ModelAction.__init__(self, 'window_shgc')

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        ModelAction.set_datalist(self, datalist)

#########TEST CODE###############
# wp = WindowProperty('ip')
# a = [1.1,2.2,3.3]
# wp.add_uvalue_list(a)
# b = [0.2,0.3,0.4,0.6]
# wp.add_shgc_list(b)
# print(wp.get_num_combination())

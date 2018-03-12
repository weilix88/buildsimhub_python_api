from .model_action import ModelAction

# The infiltration has default values
# that is determined based on standards (PNNL models)
# These default values will be used for default parametric exploration


class Infiltration(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'infiltration')

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        for i in range(len(datalist)):
            if datalist[i] > 1:
                return False
        ModelAction.set_datalist(self, datalist)

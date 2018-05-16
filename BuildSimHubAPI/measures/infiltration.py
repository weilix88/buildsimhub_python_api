from .model_action import ModelAction

# The infiltration has default values
# that is determined based on standards (PNNL models)
# These default values will be used for default parametric exploration


class Infiltration(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'infiltration')
        self._default_list = [-1, -2, -3]

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        ModelAction.set_datalist(self, datalist)

from .model_action import ModelAction


class CoolingChillerCOP(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'cooling_chillers')

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        # this is just a on off option
        ModelAction.set_datalist(self, datalist)

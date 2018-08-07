from .model_action import ModelAction


class HeatingEfficiency(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'heating_all_equip')
        self._measure_name = 'HeatingEff'
        self._lower_limit = 0
        self._upper_limit = 1

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        # this is just a on off option
        ModelAction.set_datalist(self, datalist)

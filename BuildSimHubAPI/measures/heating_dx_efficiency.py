from .model_action import ModelAction


class HeatingDXEfficiency(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'heating_dx_equip')
        self._measure_name = 'HeatCOP'
        self._lower_limit = 0

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        # this is just a on off option
        ModelAction.set_datalist(self, datalist)

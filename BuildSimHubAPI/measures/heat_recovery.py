from .model_action import ModelAction

"""

If the seed model has heat exchange object in OA system,
this measure will turn on / off the mechanical ventilation object

If the seed model has no heat exchange object but the decision value is 1 (On)
This measure will insert heat exchange object - 
With: 0.7 at 100% sensible heating and 0.75 at 100% sensible cooling

"""


class HeatRecovery(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'heat_recovery')
        self._default_list = [1, 0]
        self._data = 1
        self._measure_name = 'HeatRecovery'
        self._lower_limit = 0
        self._upper_limit = 1

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        # this is just a on off option
        ModelAction.set_datalist(self, self._default_list)

    def set_min(self, min_val):
        ModelAction.set_min(self, 0)

    def set_max(self, max_val):
        ModelAction.set_max(self, 1)

from .model_action import ModelAction

"""

If the seed model has mechanical ventilation object,
this measure will turn on / off the mechanical ventilation object


If the seed model has no mechanical ventilation object but the decision value is 1 (On)
This measure will insert mechanical ventilation object - 
based on original zone OA design and OA distribution effectiveness

If OA design is missing - insert typical office space OA using sum method (ASHRAE 62.1)
If OA distribution effectiveness is missing - insert 1.0 (Cooling) 0.8 (Heating) method (ASHRAE 90.1)

"""


class DemandControl(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'demand_control')
        self._default_list = [1, 0]
        self._data = 1
        self._measure_name = 'DemandControl'
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

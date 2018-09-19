from .model_action import ModelAction


class OccupancySensor(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'occupancy_sensor')
        self._default_list = [1, 0]
        self._data = 1
        self._measure_name = 'OccupancySensor'
        self._lower_limit = 0
        self._upper_limit = 1
        self._measure_help = '''
            measure name: OccupancySensor
            Unit: Not required
            Minimum: 0 (Off)
            Maximum: 1 (On)
            Type: Categorical (On/Off)

            Implementation logic:
            This follows the ASHRAE Appendix G guide - 10% or 15% credit is given depending on the space area.
            '''

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        # this is just a on off option
        ModelAction.set_datalist(self, self._default_list)

    def set_min(self, min_val):
        ModelAction.set_min(self, 0)

    def set_max(self, max_val):
        ModelAction.set_max(self, 1)

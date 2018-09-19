from .model_action import ModelAction


class DaylightingSensor(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'daylight_sensor')
        self._default_list = [1, 0]
        self._data = 1
        self._measure_name = 'DaylitSensor'
        self._lower_limit = 0
        self._upper_limit = 1
        self._measure_help = '''
        measure name: DaylitSensor
        Unit: Not required
        Minimum: 0 (Off)
        Maximum: 1 (On)
        Type: Categorical (On/Off)
        
        Implementation logic:
        If Off (0):
            If there is daylight sensor activated in the model - turn it off with a off schedule
            If there is no daylight sensor in the model - skip
        else if On (1):
            If there is daylight sensor activated in the model - skip
            If there is daylight sensor but not activated - turn it on with an on schedule
            If there is no daylight sensor - add a daylight sensor in the middle of the zone and turn it on.
        
        The default daylight sensor Illuminance Setpoint is set to 400 lux with a continous dimming strategy.
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

from .model_action import ModelAction

"""
If the seed model has displacement ventilation object,
this measure will delete or keep the related objects


If the seed model has no displacement ventilation object but the decision value is 1 (On)
This measure will insert room air model objects for zones under the control of central air systems

The room air model type is set to three node displacement ventilation
Default setting for the model is:
Number of Plumes per Occupant: 1
Thermostat Height: 1.1 m
Comfort Height: 1.1 m
Temperature Difference Threshold for Reporting: 0.4

Use design template to configure your DV specifications.
"""


class DisplacementVentilation(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'displace_vent')
        self._default_list = [1, 0]
        self._data = 1
        self._measure_name = 'DisplacementVent'
        self._lower_limit = 0
        self._upper_limit = 1
        self._measure_help = '''
        measure name: DisplacementVent
        Unit: Not required
        Minimum: 0 (Off)
        Maximum: 1 (On)
        Type: Categorical (On/Off)

        If the seed model has displacement ventilation object, this measure will delete or keep the related objects

        If the seed model has no displacement ventilation object but the decision value is 1 (On)
        This measure will insert room air model objects for zones under the control of central air systems

        The room air model type is set to three node displacement ventilation
        Default setting for the model is:
        Number of Plumes per Occupant: 1
        Thermostat Height: 1.1 m
        Comfort Height: 1.1 m
        Temperature Difference Threshold for Reporting: 0.4

        Use design template to configure your DV specifications.
        
        Warning: This measure only works on HVAC systems with central air handling unit.
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
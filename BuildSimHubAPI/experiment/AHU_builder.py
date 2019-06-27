from .hvac_component import HVACComponent
from .hvac_component import Component


class AHUBuilder(object):

    def __init__(self):
        self._oa_component_list = []
        self._component_list = []
        self._zone_terminal_list = []

        self._primary_heating_coil_name = ''
        self._primary_cooling_coil_name = ''
        self._supply_fan_name = ''
        self._return_fan_name = ''
        self._availability_manager_name = ''
        self._heating_water_loop = False
        self._cooling_water_loop = False

        self._doas = False
        self._unitary_sys_loop = False
        self._conditioned_zone_group = dict()
        self._conditioned_zone_group_terminal_unit = dict()

    def is_doas(self):
        self._doas = True

    def is_unitary_sys(self):
        if len(self._component_list) > 2:
            print('Error!: There are more than 2 AHU components in the loop - clear all the components and '
                  'restart the process as unitary system loop')
            return
        self._unitary_sys_loop = True

    def add_zone_terminal_component(self, component):
        if not isinstance(component, HVACComponent):
            print("Only HVAComponent can be added to the AHU component list")
            return None
        self._zone_terminal_list.append(component)

    def add_oa_component(self, component, index=None):
        if not isinstance(component, HVACComponent):
            print("Only HVAComponent can be added to the AHU component list")
            return None
        if index is None:
            self._oa_component_list.append(component)
        else:
            self._oa_component_list.insert(index, component)

    def add_component(self, component, index=None):
        if not isinstance(component, HVACComponent):
            print("Only HVAComponent can be added to the AHU component list")
            return None
        if index is None:
            self._component_list.append(component)
        else:
            self._component_list.insert(index, component)

        if component.get_component_type() == Component.primary_cooling:
            self._primary_cooling_coil_name = component.get_component_name()
            if component.required_cooling_water():
                self._cooling_water_loop = True

        elif component.get_component_type() == Component.primary_heating:
            self._primary_heating_coil_name = component.get_component_name()
            if component.required_heating_water():
                self._heating_water_loop = True

        elif component.get_component_type() == Component.fan_supply:
            self._supply_fan_name = component.get_component_name()
        elif component.get_component_type() == Component.fan_return:
            self._return_fan_name = component.get_component_name()
        elif component.get_component_type() == Component.availability_manager:
            self._availability_manager_name = component.get_component_name()

    def get_airloop_request(self):
        if not self._zone_terminal_list:
            print('Error: No zone air terminal component is defined')
            return
        if not self._oa_component_list:
            print('Error: No outdoor air component is defined')
            return
        if not self._component_list:
            print('Error: No air loop component is defined')

        if self._heating_water_loop:
            print('Warning: This air loop requires heating water loop. Make sure the heating water loop is defined')

        if self._cooling_water_loop:
            print('Warning: This air loop requires chilled water loop. Make sure the chilled water loop is defined')

        airloop_request = dict()
        airloop_request['oa'] = []
        for component in self._oa_component_list:
            airloop_request['oa'].append(component.get_component_in_json())

        airloop_request['air_loop'] = []
        for component in self._component_list:
            airloop_request['air_loop'].append(component.get_component_in_json())

        airloop_request['zone_terminal'] = [self._zone_terminal_list[0].get_component_in_json()]

        return airloop_request

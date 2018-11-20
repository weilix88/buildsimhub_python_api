from .hvac_component import HVACComponent
from .hvac_component import Component

class AHUBuilder(object):

    def __init__(self):
        self._oa_component_list = []
        self._component_list = []

        self._primary_heating_coil_name = ''
        self._primary_cooling_coil_name = ''
        self._supply_fan_name = ''
        self._return_fan_name = ''
        self._availability_manager_name = ''

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
        elif component.get_component_type() == Component.primary_heating:
            self._primary_heating_coil_name = component.get_component_name()
        elif component.get_component_type() == Component.fan_supply:
            self._supply_fan_name = component.get_component_name()
        elif component.get_component_type() == Component.fan_return:
            self._return_fan_name = component.get_component_name()
        elif component.get_component_type() == Component.availability_manager:
            self._availability_manager_name = component.get_component_name()


from enum import Enum


class HVACComponent(object):
    def __init__(self):
        self._component_name = ''
        self._component_template = None
        self._available_list = []
        self._function = Component.primary_cooling
        self._heating_water = False
        self._cooling_water = False
        self._condenser = False

    def set_component_name(self, name):
        self._component_name = name

    def set_component_template(self, template):
        if len(self._available_list) > 0:
            class_label = template['class_label']
            for s in self._available_list:
                if class_label == s:
                    self._component_template = template

    def list_available_component(self):
        """
        List of available EnergyPlus classes for a specific component
        :return:
        """
        return self._available_list

    def print_available_components(self):
        for comp in self._available_list:
            print(comp)

    def required_heating_water(self):
        return self._heating_water

    def required_cooling_water(self):
        return self._cooling_water

    def get_component_name(self):
        return self._component_name

    def get_component_in_json(self):
        comp_js = dict()
        if self._component_template is not None:
            for key in self._component_template:
                comp_js[key] = self._component_template[key]
            return comp_js

    def get_component_type(self):
        return self._function


class AHUCoilComponent(HVACComponent):
    def __init__(self, comp):
        HVACComponent.__init__(self)
        self._available_list = ['Coil:Cooling:Water', 'Coil:Cooling:Water:DetailedGeometry',
                                'Coil:Cooling:DX:SingleSpeed', 'Coil:Cooling:DX:TwoSpeed',
                                'Coil:Cooling:DX:MultiSpeed', 'Coil:Cooling:DX:VariableSpeed',
                                'Coil:Heating:Water', 'Coil:Heating:Steam', 'Coil:Heating:Electric',
                                'Coil:Heating:Electric:MultiStage', 'Coil:Heating:Fuel', 'Coil:Heating:Gas:MultiStage']
        if not isinstance(comp, Component):
            raise Exception('User Component Enum to specify function')
        self._function = comp

    def get_component_in_json(self):
        coil_json = dict()
        if self._component_template is not None:
            class_label = self._component_template['class_label']
            class_info = class_label.split(':')
            comp_function = class_info[1]
            comp_source = class_info[2]

            coil_json['coil_func'] = comp_function
            coil_json['coil_source'] = comp_source

            if comp_function == 'Heating':
                if comp_source == 'Water':
                    self._heating_water = True
            elif comp_function == 'Cooling':
                if comp_source == 'Water':
                    self._cooling_water = True

            for key in self._component_template:
                coil_json[key] = self._component_template[key]
            return coil_json
        return None


class AHUFanComponent(HVACComponent):
    def __init__(self, comp):
        HVACComponent.__init__(self)
        self._available_list = ['Fan:SystemModel', 'Fan:ConstantVolume', 'Fan:VariableVolume',
                                'Fan:OnOff']
        if not isinstance(comp, Component):
            raise Exception('User Component Enum to specify function')
        self._function = comp


class UnitaryAHUComponent(HVACComponent):
    def __init__(self, comp):
        HVACComponent.__init__(self)
        self._available_list = ['AirLoopHVAC:UnitarySystem', 'AirLoopHVAC:Unitary:Furnace:HeatOnly',
                                'AirLoopHVAC:Unitary:Furnace:HeatCool', 'AirLoopHVAC:UnitaryHeatOnly',
                                'AirLoopHVAC:UnitaryHeatCool', 'AirLoopHVAC:UnitaryHeatPump:AirToAir',
                                'AirLoopHVAC:UnitaryHeatPump:WaterToAir',
                                'AirLoopHVAC:UnitaryHeatCool:VAVChangeoverBypass',
                                'AirLoopHVAC:UnitaryHeatPump:AirToAir:MultiSpeed']


class ZoneTerminalComponent(HVACComponent):
    def __init__(self, comp):
        HVACComponent.__init__(self)
        self._available_list = ['AirTerminal:SingleDuct:Uncontrolled', 'AirTerminal:SingleDuct:ConstantVolume:Reheat',
                                'AirTerminal:SingleDuct:ConstantVolume:NoReheat', 'AirTerminal:SingleDuct:VAV:NoReheat',
                                'AirTerminal:SingleDuct:VAV:Reheat',
                                'AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan',
                                'AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat',
                                'AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat',
                                'AirTerminal:SingleDuct:SeriesPIU:Reheat',
                                'AirTerminal:SingleDuct:ParallelPIU:Reheat',
                                'AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction',
                                'AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam',
                                'AirTerminal:SingleDuct:ConstantVolume:CooledBeam',
                                'AirTerminal:SingleDuct:Mixer']
        if not isinstance(comp, Component):
            raise Exception('User Component Enum to specify function')
        self._function = comp


class Component(Enum):
    primary_heating = 1
    primary_cooling = 2
    pre_heating = 3
    pre_cooling = 4
    fan_supply = 5
    fan_return = 6
    heat_exchanger = 7
    humidifier = 8
    availability_manager = 9


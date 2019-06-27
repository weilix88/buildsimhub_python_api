from enum import Enum


class WaterLoopComponent(object):
    def __init__(self):
        self._component_name = ''
        self._component_template = None
        self._function = WaterComponent.chiller


class WaterComponent(Enum):
    chiller = 1
    boiler = 2
    condenser = 3
    pump = 4
    heatexchanger = 5

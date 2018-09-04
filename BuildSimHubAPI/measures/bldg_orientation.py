
from .model_action import ModelAction
'''
The building orientation in degrees

for example:
30 means 30 degree to the north axis.

up to 360
minimum is 0

'''


class BuildingOrientation(ModelAction):
    def __init__(self):
        ModelAction.__init__(self, 'bldg_orientation')
        self._measure_name = "Orientation"



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
        self._measure_help = '''
        measure name: Orientation
        Unit: Not required
        Minimum: 0
        Maximum: 360
        Type: numeric
        
        This measure will update the North Axis field under the Building Class.
        It will change the orientation of the building.
        '''
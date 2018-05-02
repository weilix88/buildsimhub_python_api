
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

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        ModelAction.set_datalist(self, datalist)

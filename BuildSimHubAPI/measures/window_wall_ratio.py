from .model_action import ModelAction

#this class applies overall wwr - no orientation specified
class WindowWallRatio(ModelAction):

    def __init__(self):
        ModelAction.__init__(self, 'window_wall_ratio')

    def get_num_value(self):
        return ModelAction.num_of_value(self)
from .model_action import ModelAction


# this class applies overall wwr - no orientation specified


class WindowWallRatio(ModelAction):

    def __init__(self, orientation=None):

        if orientation is None:
            ModelAction.__init__(self, 'window_wall_ratio')
            self._measure_name = 'WWR'
        else:
            orientation = orientation.lower()
            if orientation == 'w':
                ModelAction.__init__(self, 'window_wall_ratio_w')
                self._measure_name = 'WWRW'
            elif orientation == 'e':
                ModelAction.__init__(self, 'window_wall_ratio_e')
                self._measure_name = 'WWRE'
            elif orientation == 's':
                ModelAction.__init__(self, 'window_wall_ratio_s')
                self._measure_name = 'WWRS'
            elif orientation == 'n':
                ModelAction.__init__(self, 'window_wall_ratio_n')
                self._measure_name = 'WWRN'
            else:
                ModelAction.__init__(self, 'window_wall_ratio')
                self._measure_name = 'WWR'
        self._lower_limit = 0
        self._upper_limit = 1
        self._measure_help = '''
        measure name: WWR[Orientation]
        Unit: Not required
        Minimum: 0.1
        Maximum: 1.0
        Type: numeric

        This measure will readjust the window size based on current WWR and target WWR for building or a 
        specific orientation
        '''
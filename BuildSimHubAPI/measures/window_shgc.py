from .model_action import ModelAction


class WindowSHGC(ModelAction):

    def __init__(self, orientation=None):
        if orientation is None:
            ModelAction.__init__(self, 'window_shgc')
            self._measure_name = 'Window_SHGC'
        else:
            orientation = orientation.lower()
            if orientation == 'w':
                ModelAction.__init__(self, 'window_shgc_w')
                self._measure_name = 'Window_SHGC_West'
            elif orientation == 'e':
                ModelAction.__init__(self, 'window_shgc_e')
                self._measure_name = 'Window_SHGC_East'
            elif orientation == 's':
                ModelAction.__init__(self, 'window_shgc_s')
                self._measure_name = 'Window_SHGC_South'
            elif orientation == 'n':
                ModelAction.__init__(self, 'window_shgc_n')
                self._measure_name = 'Window_SHGC_North'
            else:
                ModelAction.__init__(self, 'window_shgc')
                self._measure_name = 'Window_SHGC'
        self._lower_limit = 0
        self._upper_limit = 1
        self._measure_help = '''
        measure name: Window_SHGC_[Orientation]
        Unit: ip or si
        Minimum: 0.1
        Maximum: 1.0
        Type: numeric

        This measure will update the SHGC of the window in WindowMaterial:SimpleGlazingSystem 
        It is suggested to use this function with Window Uvalue measure - if the Window U-Value is not present
        and the original model uses detail window layer method, then this measure could create a new simple glazing system
        with a default U-value.
        '''

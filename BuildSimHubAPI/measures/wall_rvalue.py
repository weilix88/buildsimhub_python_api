from .model_action import ModelAction


class WallRValue(ModelAction):
    # this shows the ip to si conversion rate
    # if unit is 'ip', then multiply this rate.
    # for window it is the U-value
    # convert U-value IP to SI
    CONVERSION_RATE = 5.678

    def __init__(self, unit="si"):
        ModelAction.__init__(self, 'wall_rvalue', unit)
        self._measure_name = 'Wall_R'
        self._lower_limit = 0

    def _unit_convert_ratio(self):
        return WallRValue.CONVERSION_RATE

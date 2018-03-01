import matplotlib.pyplot as plt

class ParametricResult():
    BASE_URL = 'https://develop.buildsimhub.net'

    def __init__(self, model_keys):
        self._model_keys = model_keys

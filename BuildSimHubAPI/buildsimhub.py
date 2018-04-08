from BuildSimHubAPI import helpers


class BuildSimHubAPIClient:
    """
    This BuildSimHub API client
    use this object to interact with the v1 API. for example:

    """
    def __init__(self):
        """
        Construct BuildSimHub v1 API object
        """

        info = helpers.bldgsim_info.MetaInfo()
        self._userAPI = info.user_key
        self._base_url = info.base_url

    @property
    def user_api(self):
        return self._userAPI

    def new_simulation_job(self, model_key=""):
        sj = helpers.simulation_job.SimulationJob(self._userAPI, model_key, self._base_url)
        return sj

    def new_parametric_job(self, model_key):
        # type: (object) -> object
        pj = helpers.parametric_job.ParametricJob(self._userAPI, model_key, self._base_url)
        return pj

    def get_model(self, simulationJob):
        model_key = vars(simulationJob)['_track_token']
        test = model_key.split("-")
        if len(test) is not 3:
            model_key = vars(simulationJob)['_model_key']

        model = helpers.energy_model.Model(self._userAPI, model_key, self._base_url)
        return model

    def get_parametric_results(self, parametricJob):
        model_key = vars(parametricJob)['_track_token']
        return helpers.parametric_model.ParametricModel(self._userAPI, model_key, self._base_url)


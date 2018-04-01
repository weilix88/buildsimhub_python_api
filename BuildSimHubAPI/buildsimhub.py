from BuildSimHubAPI import helpers


class BuildSimHubAPIClient:
    """
    This BuildSimHub API client
    use this object to interact with the v1 API. for example:
    bsh = buildsimhub.BuildSimHubAPIClient(apikey = os.environ.get('BUILDSIMHUB_API_KEY'))

    """
    def __init__(self):
        """
        Construct BuildSimHub v1 API object

        :params host: Base URL for the API call
        :type host: String
        :param apikey: BuildSimHub API key to use. Defaults to environment var
        :type apikey: string
        """
        info = helpers.bldgsim_info.MetaInfo()
        self._userAPI = info.user_key
        self._base_url = info.base_url

    @property
    def userAPI(self):
        return self._userAPI

    def new_simulation_job(self, model_key=""):
        sj = helpers.simulation_job.SimulationJob(self._userAPI, model_key, self._base_url)
        return sj

    def new_parametric_job(self, model_key):
        # type: (object) -> object
        pj = helpers.parametric_job.ParametricJob(self._userAPI, model_key, self._base_url)
        return pj

    def get_simulation_type(self):
        st = helpers.simulation_type.SimulationType()
        return st

    def get_model(self, simulationJob):
        model_key = vars(simulationJob)['_trackToken']
        test = model_key.split("-")
        if len(test) is not 3:
            model_key = vars(simulationJob)['_modelKey']

        model = helpers.energy_model.Model(self._userAPI, model_key, self._base_url)
        return model

    def get_parametric_results(self, parametricJob):
        model_key = vars(parametricJob)['_trackToken']
        return helpers.parametric_model.ParametricModel(self._userAPI, model_key, self._base_url)


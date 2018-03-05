from BuildSimHubAPI import helpers

class BuildSimHubAPIClient():
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
        self._userAPI = info.userKey

    @property
    def userAPI(self):
        return self._userAPI

    def new_simulation_job(self, model_key=""):
        sj = helpers.simulation_job.SimulationJob(self._userAPI, model_key)
        return sj

    def new_parametric_job(self, model_key):
        # type: (object) -> object
        pj = helpers.parametric_job.ParametricJob(self._userAPI, model_key)
        return pj

    def get_simulation_type(self):
        st = helpers.simulation_type.SimulationType()
        return st

    def get_model(self, simulationJob):
        modelKey = vars(simulationJob)['_trackToken']
        model = helpers.energy_model.Model(self._userAPI,modelKey)
        return model

    def get_parametric_results(self, parametricJob):
        modelKey = vars(parametricJob)['_trackToken']
        return helpers.parametric_model.ParametricModel(self._userAPI, modelKey)


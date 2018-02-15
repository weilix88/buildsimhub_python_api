from BuildSimHubAPI.helpers import bldgsim_info
from BuildSimHubAPI.helpers import simulationJob
from BuildSimHubAPI.helpers import simulationType

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
        info = bldgsim_info.MetaInfo()
        self._userAPI = info.userKey

    @property
    def userAPI(self):
        return self._userAPI

    def new_simulation_job(self, model_key):
        sj = simulationJob.SimulationJob(self._userAPI, model_key)
        return sj

    def get_simulation_type(self):
        st = simulationType.SimulationType()
        return st

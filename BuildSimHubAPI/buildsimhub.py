"""
This library allows you to quickly and easily use the BuildSim API via Python.

For more information on this library, see the README on Github.
    https://github.com/weilix88/buildsimhub_python_api/blob/master/README.md
For more information on the BuildSim API, see the API openAPI specification
    https://github.com/weilix88/buildsimhub_python_api/blob/master/bsh_openapi.yaml

This file provides the BuildSim API client
"""

from BuildSimHubAPI import helpers


class BuildSimHubAPIClient(object):
    """
    This BuildSimHub API client
    use this object to interact with the BuildSim API. for example:
    bsh = buildsimhub.BuildSimHubAPI()
    ...
    new_simulation = bsh.new_simulation_job()
    response = new_simulation.run("in.idf","in.epw",track=True)

    For examples and detailed use instructions, see:
        https://github.com/weilix88/buildsimhub_python_api

    """

    def __init__(self):
        """
        Construct BuildSimHub API object

        user_api and base_url should specified in the info.config
        in the API package
        """
        info = helpers.bldgsim_info.MetaInfo()
        self._user_api = info.user_key
        self._base_url = info.base_url

    @property
    def user_api(self):
        """User Key"""
        return self._user_api

    def new_simulation_job(self, model_key=""):
        """
        Generate a new simulation job

        :param model_key: optional param, only supplied if a project is created on BuildSimHub platform
        :return: a simulation job object
        :rtype: SimulationJob or None

        """
        sj = helpers.simulation_job.SimulationJob(self._user_api, model_key, self._base_url)
        return sj

    def new_parametric_job(self, model_key):
        """
        Generate a new parametric job

        :param model_key: required param.
        :return: a parametric job object
        :rtype: ParametricJob or None

        """
        # type: (object) -> object
        pj = helpers.parametric_job.ParametricJob(self._user_api, model_key, self._base_url)
        return pj

    def get_simulation_results(self, simulation_job):
        """
        Generate the simulation result object

        :param simulation_job: required - a valid simulation job with a track_token / a model_key
        :return: Model or None

        """
        model_key = vars(simulation_job)['_track_token']
        test = model_key.split("-")
        if len(test) is not 3:
            model_key = vars(simulation_job)['_model_key']

        model = helpers.energy_model.Model(self._user_api, model_key, self._base_url)
        return model

    def get_parametric_results(self, parametric_job):
        """
        Generate parametric simulation study result object

        :param parametric_job:
        :return: ParametricModel or None
        """
        model_key = vars(parametric_job)['_track_token']
        return helpers.parametric_model.ParametricModel(self._user_api, model_key, self._base_url)

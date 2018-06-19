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

    def __init__(self, base_url=None):
        """
        Construct BuildSimHub API object

        user_api and base_url should specified in the info.config
        in the API package
        """
        info = helpers.bldgsim_info.MetaInfo()

        if base_url is None:
            self._base_url = info.base_url
        else:
            self._base_url = base_url

    def model_results(self, project_key, model_key):
        """
        retrieve a model's results based on project key and model key

        :param project_key: the key to access the project e.g. f698f06-4388-549-8a29-e227d7b696
        :param model_key: the key to access the model, it can be:
        a7ce63-0e58-4efc-93f3-73b7ddaa0 or 111-111-111
        :return: the model results
        """
        results = helpers.Model(project_key, model_key, self._base_url)
        return results

    def parametric_results(self, project_key, model_key):
        """
        retrieve a parametric study results based on project key and model key

        :param project_key: the key to access the project e.g. f698f06-4388-549-8a29-e227d7b696
        :param model_key: the key to access the model. e.g. a7ce63-0e58-4efc-93f3-73b7ddaa0
        :return: the parametric results

        """
        results = helpers.ParametricModel(project_key, model_key, self._base_url)
        return results

    def new_simulation_job(self, project_key):
        """
        Generate a new simulation job

        :param project_key: required param, only supplied if a project is created on BuildSimHub platform
        :return: a simulation job object
        :rtype: SimulationJob or None

        """
        sj = helpers.simulation_job.SimulationJob(project_key, self._base_url)
        return sj

    def new_parametric_job(self, project_key, model_key=""):
        """
        Generate a new parametric job

        :param project_key: required
        :param model_key: required param.
        :return: a parametric job object
        :rtype: ParametricJob or None

        """
        pj = helpers.parametric_job.ParametricJob(project_key, model_key, self._base_url)
        return pj

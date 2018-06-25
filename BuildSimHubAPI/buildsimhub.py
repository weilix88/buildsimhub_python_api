"""
This library allows you to quickly and easily use the BuildSim API via Python.

For more information on this library, see the README on Github.
    https://github.com/weilix88/buildsimhub_python_api/blob/master/README.md
For more information on the BuildSim API, see the API openAPI specification
    https://github.com/weilix88/buildsimhub_python_api/blob/master/bsh_openapi.yaml

This file provides the BuildSim API client
"""

from BuildSimHubAPI import helpers
from BuildSimHubAPI.helpers.httpurllib import request_large_data
# from BuildSimHubAPI.helpers.network_connectivity import internet


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

        # Check internet connection - this code is not using in the API library for now
        # if not internet():
        #    print("Cannot connect with internet - please check your internet settings")
            # force to stop process.
        #     exit()
        # else:
        #     print("Connected with internet - Lets start!")

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

    def model_list(self, project_key, model_key):
        """
        This method retrieves all the model history of one model
        For parametric run, this means retrieve all the model information under one
        parametric run.

        :param project_key:
        :param model_key:
        :return:
        """
        url = self._base_url + 'GetModelHistoryKey_API'
        payload = {
            'project_api_key': project_key,
            'folder_api_key': model_key
        }

        data_list = request_large_data(url, params=payload)
        return data_list

    def project_model_list(self, project_key):
        """
        This method retrieves all the model information under a project

        :param project_key:
        :return:
        """
        url = self._base_url + 'GetModelList_API'
        payload = {
            'project_api_key': project_key
        }
        data_list = request_large_data(url, params=payload)
        return data_list

import requests
def get_simulation_results():

        url = 'https://develop.buildsimhub.net/GetSimulationResult_API'
        payload = {
            'user_api_key': '94266512-c5ea-463d-a108-9dd1e84c07ca',
            'result_type': 'html',
            'track_token': '323|861|2369'
        }

        r = requests.post(url, params=payload, stream=True)

        f = ""
        if r.status_code == 200:
            f = r.text
        return f



r = get_simulation_results()
print(r)
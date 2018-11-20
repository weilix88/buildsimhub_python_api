from .httpurllib import request_get
import json


class ClassTemplate(object):
    # every call will connect to this base URL
    BASE_URL = 'https://my.buildsim.io/'

    def __init__(self, project_api_key, track_token, class_label, base_url=None, logger=None):

        self._project_api_key = project_api_key
        self._track_token = track_token
        self._base_url = ClassTemplate.BASE_URL
        self._class_label = class_label
        self._logger = None
        self._required = False
        self._num_field = 0
        self._min_field = 0
        self._field_list = None

        if logger is not None:
            self._logger = logger

        if base_url is not None:
            self._base_url = base_url

        track = 'folder_api_key'
        test = self._track_token.split('-')
        if len(test) is 3:
            track = 'track_token'

        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
            'class_label': class_label
        }
        url = self._base_url + 'GetClassTemplate_API'
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
        if resp_json['status'] == 'success':
            data = resp_json['data']
            if 'required' in data:
                self._required = True
            if 'field_min' in data:
                self._min_field = data['field_min']
            if 'field_num' in data:
                self._num_field = data['field_num']
            if 'field_detail' in data:
                self._field_list = data['field_detail']

    def get_raw_data(self):
        return self._field_list

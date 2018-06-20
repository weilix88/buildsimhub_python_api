"""
This post-process class that transform the model_list data
[{'commit_msg': 'WWR: 0.4, LPD: 0.9, HeatingEff: 0.86', 'commit_user': 'API user', 'commit_date': '2018-06-20',
'commit_id': '1-146-429'}, {'commit_msg': 'WWR: 0.4, LPD: 0.9, HeatingEff: 0.8', 'commit_user': 'API user',
'commit_date': '2018-06-20', 'commit_id': '1-146-428'}]
to pandas dataframe

It is required for pandas dataframe
"""
import os

try:
    import pandas as pd
except ImportError:
    pd = None
    print('pandas is not installed')


class ModelList(object):

    def __init__(self, data):
        self._df = pd.DataFrame(data)

    def pandas_df(self):
        return self._df



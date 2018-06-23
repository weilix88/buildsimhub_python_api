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
        # drop the row whose commit_msg is INIT
        self._df = self._df[self._df.commit_msg != 'INIT']

    def pandas_df(self):
        return self._df

    def parametric_df(self):
        """
        This function rearrange the Dataframe by splitting the commit message into parameters

        :return:
        """
        param_list = list()
        for index, row in self._df.iterrows():
            msg = row['commit_msg']
            parameters = msg.split(",")
            data_dict = dict()
            for k in range(len(parameters)):
                title, val = parameters[k].split(":")
                # for cases like on off options
                data_dict[title.strip()] = float(val.strip())
            param_list.append(data_dict)
        parameter_df = pd.DataFrame(param_list)
        return pd.concat([self._df, parameter_df], axis=1)









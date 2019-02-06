from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint as sp_randint
from scipy.stats import uniform as sp_randuni
import numpy as np


class Regressor(object):

    def __init__(self, df):
        self._data = df
        self._data_type = list()
        self._alg = None
        self._feature_list = dict()
        self._header_list = []
        self._hyper_param_spec = dict()
        self._alg_name = 'regressor'

    def alg_name(self):
        return self._alg_name

    def grid_search_cv(self, target):
        param_dist = dict()
        for key in self._hyper_param_spec:
            key_info = self._hyper_param_spec[key]
            key_type = key_info['type']
            if key_type == 'num':
                param_dist[key] = sp_randuni(key_info['min'], key_info['max'])
            elif key_type == 'int':
                param_dist[key] = sp_randint(key_info['min'], key_info['max'])
            elif key_type == 'bool':
                param_dist[key] = key_info['bool']
            elif key_type == 'choice':
                param_dist[key] = key_info['choice']

        temp_df = self._data.copy()
        target_data = np.array(temp_df[target])
        del temp_df[target]

        temp_df = self._df_encoder(temp_df)
        features = np.array(temp_df)

        # run randomized search
        n_iter_search = 40
        random_search = RandomizedSearchCV(self.get_alg(), param_distributions=param_dist,
                                           n_iter=n_iter_search, cv=5)
        random_search.fit(features, target_data)
        results = random_search.cv_results_
        rank_ind = results['rank_test_score'][0]
        params = results['params'][rank_ind-1]

        for key in params:
            self._hyper_param_spec[key]['val'] = params[key]

    def get_alg(self):
        """
        Get the algorithm with default hyperparameters
        :return:
        """
        pass

    def train(self, target):
        """
        alg training method - train the algorithm with data
        include 3 steps:
        1. Data processing - process data using One-Hot Encoding or labelencoding
        2. Apply hyperparameters
        3. return test
        :param target: str, the name of the target value
        :return: predicted errors [mean absolute error, mean squared error]
        """
        pass

    def predict(self, test):
        """
        Test should be in the format of pandas dataframe
        1. Data processing - should be exactly as the training process

        :param test: pandas df
        :return: list of predicted values
        """
        pass

    def _df_encoder(self, temp_df):
        """
        static encoding the dataframe
        :return:
        """
        pass

    def _feature_extract(self, temp_df):
        categorical_df = temp_df.select_dtypes(include=[object])
        if not categorical_df.empty:
            # 1. INSTANTIATE
            header_list = list(categorical_df)
            for head in header_list:
                self._feature_list[head] = dict()
                self._feature_list[head]['type'] = 'cat'
                self._feature_list[head]['choice'] = categorical_df[head].unique().tolist()

        header_list = list(temp_df)
        max_list = temp_df.max().tolist()
        min_list = temp_df.min().tolist()
        for i in range(len(header_list)):
            head = header_list[i]
            if head not in self._feature_list:
                self._feature_list[head] = dict()
                self._feature_list[head]['type'] = 'num'
                self._feature_list[head]['max'] = max_list[i]
                self._feature_list[head]['min'] = min_list[i]

    def get_feature_list(self):
        return self._feature_list

    def get_header_list(self):
        return self._header_list

    def hyper_parameter_spec(self):
        return self._hyper_param_spec

    def set_hyper_parameter_spec(self, parameter):
        for key in parameter:
            if key in self._hyper_param_spec:
                self._hyper_param_spec[key]['val'] = parameter[key]['val']

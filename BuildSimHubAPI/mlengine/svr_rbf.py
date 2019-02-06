from .regressor import Regressor
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn import preprocessing


class SVRRBF(Regressor):
    def __init__(self, df):
        Regressor.__init__(self, df)
        self._alg_name = 'SVR-RBF Kernel'
        self._copied_data = self._data.copy()
        self._hyper_param_spec['C'] = {'type': 'num', 'min': 2**-5, 'max': 2**15, 'default': 16, 'val': 16}
        self._label_converter = dict()

    def train(self, target):
        temp_df = self._copied_data
        target_data = temp_df[target]
        del temp_df[target]
        self._header_list = list(temp_df)
        self._feature_extract(temp_df)

        # try encode categorical data
        temp_df = self._df_encoder(temp_df)
        features = np.array(temp_df)

        # retrieve from the hyper parameter spec
        test_size = 0.2
        C = self._hyper_param_spec['C']['val']

        x_train, x_test, y_train, y_test = train_test_split(features, target_data, test_size=test_size)
        self._alg = SVR(kernel='rbf', C=C, gamma='auto')
        self._alg.fit(x_train, y_train)
        pred_linear = self._alg.predict(x_test)

        return [metrics.mean_absolute_error(y_test, pred_linear), metrics.mean_squared_error(y_test, pred_linear)]

    def predict(self, test):
        if self._alg is None:
            return 'Error: No algorithm is trained'
        val_df = pd.DataFrame(test, index=[0])
        temp_df = self._df_encoder(val_df)
        features = np.array(temp_df)
        return self._alg.predict(features)

    def get_alg(self):
        return SVR(kernel='rbf', C=16, gamma='auto')

    def _df_encoder(self, temp_df):
        categorical_df = temp_df.select_dtypes(include=[object])
        if not categorical_df.empty:
            head_list = list(categorical_df)
            for head in head_list:
                if head not in self._label_converter:
                    le = preprocessing.LabelEncoder()
                    le.fit(categorical_df[head])
                    self._label_converter[head] = le
                    temp_df[head] = le.transform(temp_df[head])
                else:
                    temp_df[head] = self._label_converter[head].transform(temp_df[head])
        return temp_df

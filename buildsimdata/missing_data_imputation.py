# https://github.com/WillKoehrsen/feature-selector/blob/master/Feature%20Selector%20Usage.ipynb
import pandas as pd
from datetime import datetime
from .feature_selector import FeatureSelector
import math
from sklearn.neighbors import KNeighborsRegressor
import numpy as np


df = pd.read_csv('/Users/weilixu/Desktop/Bldg101_2014_10m_NA10.csv')
# test_missing = pd.read_excel('../missingdata/PI_Bldg101_Webctrl_Points.xlsx')

# Feature Selection - remove single value and high correlation variable
fs = FeatureSelector(data=df)

fs.identify_single_unique()
single_unique = fs.ops['single_unique']
df = df.drop(columns = single_unique)


fs.identify_collinear(correlation_threshold=0.975)
correlated_features = fs.ops['collinear']
df = df.drop(columns = correlated_features)

# dataframe handling

#df_copy = df
dateTime = df['timestamp'].tolist()
# print(df_copy['timestamp'].head(500))
dates_list = [datetime.strptime(index, '%m/%d/%y %H:%M').strftime('%m/%d/%y') for index in dateTime]
# print(dates_list)

month = [datetime.strptime(index, '%m/%d/%y %H:%M').strftime('%m') for index in dateTime]
# print(month)
weekofday =[datetime.strptime(index, '%m/%d/%y %H:%M').strftime('%A') for index in dateTime]
# print(weekofday)
hour =[datetime.strptime(index, '%m/%d/%y %H:%M').strftime('%H') for index in dateTime]
# print(hour)

df.insert(loc=0, column='month', value=month)
df.insert(loc=1, column='weekofday', value=weekofday)
df.insert(loc=2, column='hour', value=hour)
print(len(df))

# na_df rows have been removed from df so that we can add the row after filling missing value back to df
na_df = df[df.isnull().any(1)] # To find out which rows have NaNs
ready_before = pd.concat([df, na_df]).drop_duplicates(keep=False)
print (len(ready_before))


# The function is used to find the t1, t2 data
def nPrevHour(timeDict, n, na_df):
    '''
    Return a dictionary
    key: current hour
    value: previous n hour data
    '''
    row_fields = df_copy.keys()
    ans = {}
    for index, row in na_df.iterrows():
        weekday = row[row_fields[1]]
        currTime = row[row_fields[1]] + ' ' + row[row_fields[2]]
        # print (currTime)
        targetTime = findTargetTime(n, int(row[row_fields[2]]), weekday)
        if currTime not in ans:
            ans[currTime] = timeDict[targetTime]
            # print("Here:")

    return ans


def findTargetTime(n, hour, weekday):
    weekday_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    res = 0
    target_weekday = ''
    if hour - n < 0:
        a = weekday_list.index(weekday) - 1
        if a < 0:
            a = a + 7

        target_weekday = weekday_list[a]
        res = hour - n + 24
    else:
        target_weekday = weekday
        res = hour - n

    if res < 10:
        return target_weekday + ' ' + '0' + str(res)
    else:
        return target_weekday + ' ' + str(res)


# The part is used to generate t1 and t2 data
df_copy = df
row_fields = df_copy.keys()
timeDict = {}

for index, row in df_copy.iterrows():
    current_time = row[row_fields[1]] + ' ' + row[row_fields[2]]
    if current_time not in timeDict:
        timeDict[current_time] = []
    timeDict[current_time].append(list(row)[4:])

t0 = {} # current timm
t1 = {}
t2 = {}

t1 = nPrevHour(timeDict, 1, na_df)
t2 = nPrevHour(timeDict, 2, na_df)


# The part is to put t1 and t2 data to the current time's training set
for key, value in t1.items():
    t1[key].extend(t2[key])

# remove training date which has nan value in the list
# Reason: the list having nan cannot be used as the training data
for key, value in t1.items():
    for i in range(len(value)):
        remove = []
        for j in range(len(value[i])):
            if isinstance(value[i][j], float) and math.isnan(value[i][j]):
                remove.append(j)

        # remove.reverse()
        value[i] = [value[i][j] for j in range(len(value[i])) if j not in remove]
# for j in range(len(remove)):
#             value[i].pop(remove[j])


# seperate to training data and predict data
# here, training data is the dataset containing t1 and t2; predict data is the data having missing value
train_data = []
predict_data = []
idxToTime = {}
for index, row in na_df.iterrows():
    weekday = row[row_fields[1]]
    currTime = row[row_fields[1]] + ' ' + row[row_fields[2]]
    idxToTime[index] = currTime

for index, row in na_df.iterrows():
    predict_data.append(list(row)[4:])
    train_data.append(t1[idxToTime[index]])

# If 85% of one row is nan, the row will be removed
delete_position = []
for i in range(len(predict_data)):
    count = 0
    for j in range(len(predict_data[i])):
        if isinstance(predict_data[i][j], float) and math.isnan(predict_data[i][j]):
            count = count + 1

    if float(count) / len(predict_data[i]) > 0.8:
        delete_position.append(i)


train_data = [ train_data[i] for i in range(len(train_data)) if i not in delete_position]
predict_data = [ predict_data[i] for i in range(len(predict_data)) if i not in delete_position]


def knnTrain(predict_data, train_data):
    train_data_ = []
    train_label_ = []
    predict_data_ = []

    # preprocess data
    # 1. the length of training data is different from our data
    # 2. the data cannot be nan in trainning data (should be done before)
    len_ = len(predict_data)
    # print (predict_data)
    # len_ = len(train_data[0])
    # print(len_)
    for i in range(len(train_data)):
        if len(train_data[i]) == len_:
            train_data_.append([train_data[i][j] for j in range(len(predict_data)) if
                                isinstance(predict_data[j], float) and math.isnan(predict_data[j]) == False])
            train_label_.append([train_data[i][j] for j in range(len(predict_data)) if
                                 isinstance(predict_data[j], float) and math.isnan(predict_data[j]) == True])

    predict_data_ = [x for x in predict_data if math.isnan(x) == False]

    len_ = len(train_data_[0])
    train_label_ = [train_label_[i] for i in range(len(train_label_)) if len(train_data_[i]) == len_]
    train_data_ = [x for x in train_data_ if len(x) == len_]

    temp = np.array(train_data_)
    temp1 = np.array(train_label_)
    # print(temp)

    # train
    neigh = KNeighborsRegressor(n_neighbors=3)
    neigh.fit(temp, temp1)
    # predict
    res = neigh.predict([predict_data_])

    # put the predicted value back to row
    filled_na_data_ = [res.tolist()[0] for x in predict_data if math.isnan(x) == True]

    # add the data back to df
    new_predict_data = predict_data
    for (i, item) in enumerate(new_predict_data):
        for (j, item2) in enumerate(filled_na_data_):
            if math.isnan(item) == True:
                new_predict_data[i] = filled_na_data_[j]
    print(new_predict_data)


problem = []
for i in range(1,len(predict_data)):
    # print(i)
    knnTrain(predict_data[i], train_data[i])
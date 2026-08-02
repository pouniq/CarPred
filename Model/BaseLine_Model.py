import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.model_selection import train_test_split, cross_validate, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    root_mean_squared_error, 
    mean_squared_error, 
    mean_absolute_error,
    r2_score,
    

    )

RANDOM_STATE = 42

train = pd.read_csv('../PreProcessing/train.csv')
test = pd.read_csv('../PreProcessing/test.csv')


X_train = train[['mileage','date',"insurance"]]
y_train = train['price']

X_test = test[['mileage','date',"insurance"]]
y_test = test['price']



num_cols = X_train.columns
# cat_cols = ['color']


median = X_train['insurance'].median()
X_train['insurance'] = X_train['insurance'].fillna(median)
X_test['insurance'] = X_test['insurance'].fillna(median)

processor = ColumnTransformer([
    ('numerical columns', StandardScaler(), num_cols)
    # ('categorical columns', OneHotEncoder(drop='first', handle_unknown='ignore'), cat_cols)
])

X_train_processed = processor.fit_transform(X_train)
X_test_processed = processor.transform(X_test)

model = LinearRegression()
# model.fit(X_train_processed, y_train)


# y_pred_train = model.predict(X_train_processed)
# y_pred = model.predict(X_test_processed)

# r2_score(y_pred_train, y_train)
# r2_score(y_pred=y_pred, y_true=y_test)


# print(X_train.dtypes)
# print(X_train.describe())
# print(y_train.describe())
# print(model.coef_)
# print(np.abs(y_pred - y_test).describe()) 

# plt.scatter(y_pred_train, y_train)
# plt.scatter(y_pred, y_test)

cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
y_train_processed = np.log(y_train)
scores = cross_val_score(model,X_train_processed, y_train_processed, cv = cv, scoring='r2' )
print(scores.mean())


model.fit(X_train_processed, y_train_processed)
y_pred_train_log = model.predict(X_train_processed)
y_pred_train = np.exp(y_pred_train_log)



y_pred_log = model.predict(X_test_processed)
y_pred = np.exp(y_pred_log)

r2_score(y_pred_train, y_train)
r2_score(y_pred, y_test)




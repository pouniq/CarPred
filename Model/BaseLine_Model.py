import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.model_selection import cross_validate, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler , OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR
from joblib import dump


from sklearn.metrics import (
    root_mean_squared_error, 
    mean_squared_error, 
    mean_absolute_error,
    r2_score
    

    )

RANDOM_STATE = 42

X_train = pd.read_csv('../PreProcessing/X_train.csv')
X_test = pd.read_csv('../PreProcessing/X_test.csv') 

y_train = pd.read_csv('../PreProcessing/y_train.csv')
y_test = pd.read_csv('../PreProcessing/y_test.csv')



num_cols = ['mileage', 'date', 'insurance']
cat_cols = ['color_2_cat']
processor = ColumnTransformer([
    ('numerical columns', StandardScaler(), num_cols),
    ('categorical columns', OneHotEncoder(drop='first', handle_unknown='ignore'), cat_cols)
])

X_train_processed = processor.fit_transform(X_train)
X_test_processed = processor.transform(X_test)

y_train_processed = np.log(y_train)


model = LinearRegression()



cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

scores = cross_val_score(model,X_train_processed, y_train_processed, cv = cv, scoring='r2' )
print(scores.mean())

model.fit(X_train_processed, y_train_processed)
y_pred_train_log = model.predict(X_train_processed)
y_pred_train = np.exp(y_pred_train_log)

r2_score(y_train, y_pred_train)


y_pred_log = model.predict(X_test_processed)
y_pred = np.exp(y_pred_log)

r2_score(y_test, y_pred)

plt.scatter(y_pred_train, y_train)

root_mean_squared_error(y_test, y_pred) 


joblib_path = "/Users/pouniq/CarPrediction/Model/model_dir/baseline_linear.joblib"
dump(model, joblib_path)



###### Ridge regression model #########

ridge_model = Ridge()
ridge_model.fit(X_train_processed, y_train_processed)


y_pred_train_log_ridge = ridge_model.predict(X_train_processed)
y_pred_train_ridge = np.exp(y_pred_train_log_ridge)

r2_score(y_train, y_pred_train_ridge)


y_pred_log_ridge = ridge_model.predict(X_test_processed)
y_pred_ridge = np.exp(y_pred_log_ridge)

r2_score(y_test, y_pred_ridge)

############################################################



####### SVM REGRESSOR #####################################

model_svr = SVR()
model_svr.fit(X_train_processed, y_train_processed)

y_pred_train_log_svr = model_svr.predict(X_train_processed)
y_pred_train_svr = np.exp(y_pred_train_log_svr)

r2_score(y_train, y_pred_train_svr)


y_pred_log_svr = model_svr.predict(X_test_processed)
y_pred_svr = np.exp(y_pred_log_svr)

r2_score(y_test, y_pred_ridge)


###############################################################
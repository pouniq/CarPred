import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

from sklearn.model_selection import GridSearchCV, cross_val_score, RepeatedKFold, KFold
from sklearn.preprocessing import StandardScaler , OneHotEncoder
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR
from joblib import dump


from sklearn.metrics import (
    root_mean_squared_error, 
    mean_squared_error, 
    mean_absolute_error,
    r2_score,
    mean_absolute_percentage_error
    

    )

RANDOM_STATE = 42

X_train = pd.read_csv('../PreProcessing/X_train.csv')
X_test = pd.read_csv('../PreProcessing/X_test.csv') 

y_train = pd.read_csv('../PreProcessing/y_train.csv')
y_test = pd.read_csv('../PreProcessing/y_test.csv')


y_train = y_train.values.ravel()
y_test = y_test.values.ravel()

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

pipe = Pipeline([
    ('processor', processor),
    ('model', LinearRegression())
])

cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

scores = cross_val_score(pipe, X_train, y_train_processed, cv=cv, scoring='r2')





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

r2_score(y_test, y_pred_svr)


###############################################################


models = {
    'linear': LinearRegression(),
    'ridge': Ridge(),
    'elasticNet': ElasticNet(),
    'svr': SVR(),
    'gbr': GradientBoostingRegressor(),
    'rfr': RandomForestRegressor()
}



for name, est in models.items():
    pipe = Pipeline([('processor', processor), ('model', est)])
    scores = cross_val_score(pipe, X_train, y_train_processed, cv=cv, scoring='neg_root_mean_squared_error')
    print(f"{name}: RMSE = {-scores.mean():.3f}, std = {scores.std():.3f}")
    
    
    

    
###############################################################
###############################################################
# with more data the BEST model Become the LinearRegression

pip_best = Pipeline(
    [
        ('processor', processor),
        ("model", LinearRegression())
    ]
)

model_log = TransformedTargetRegressor(
    regressor=pip_best,
    func=np.log,
    inverse_func=np.exp
)

model_log.fit(X_train, y_train)

y_pred_train = model_log.predict(X_train)
r2_score(y_train, y_pred_train)

y_pred = model_log.predict(X_test)
r2_score(y_test, y_pred)



###############################################################
###############################################################
# Let's Tune Ridge Alpha to see whether or not we improve the model


# pip_best_R = Pipeline(
#     [
#         ('processor', processor),
#         ("model", Ridge())
#     ]
# )


# model_log = TransformedTargetRegressor(
#     regressor=pip_best_R,
#     func=np.log,
#     inverse_func=np.exp
# )

# param_grid_ridge = {
#     'regressor__model__alpha': [0,0.001, 0.01, 0.1, 1, 10, 100]
# }

# grid = GridSearchCV(
#     model_log,
#     param_grid=param_grid_ridge,
#     scoring='neg_root_mean_squared_error',
#     cv = 5,
#     n_jobs= -1,
#     verbose=1
# )

# grid.fit(X_train, y_train)
# grid.best_score_
# grid.best_params_

# y_pred_train = grid.predict(X_train)
# r2_score(y_train, y_pred_train)

# in gridsearch it is confirmed that the linear Regression is the best model for this model at this moment











## save the model

joblib_path = "/Users/pouniq/CarPrediction/Deployment/model_dir/SVR_Model.joblib"
dump(model_log, joblib_path)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

from sklearn.model_selection import GridSearchCV, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler , OneHotEncoder
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
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
    'svr': SVR(),
    'gbr': GradientBoostingRegressor(max_depth=3, n_estimators=100, random_state=RANDOM_STATE),
    'rfr': RandomForestRegressor(max_depth=5, n_estimators=200, random_state=RANDOM_STATE)
}



for name, est in models.items():
    pipe = Pipeline([('processor', processor), ('model', est)])
    scores = cross_val_score(pipe, X_train, y_train_processed, cv=cv, scoring='neg_mean_squared_error')
    print(f"{name}: MSE = {-scores.mean():.3f}, std = {scores.std():.3f}")
    
    
    
###############################################################
###############################################################
# Model Selection Ridge was choosen then SVR, gbr and rfr in order
# Now after feeding some data points the best model is randomforestRegressor

pipe = Pipeline(
    [
        ('processor', processor),
        ('model', Ridge() )
    ]
)

param_grid = {
    'model__alpha': [0.001, 0.01, 0.1, 1.0, 10, 100, 1000 ],
    
}


grid = GridSearchCV(
    pipe,
    param_grid=param_grid,
    scoring='neg_mean_squared_error',
    cv = 5
)


grid.fit(X_train, y_train_processed)

grid.best_params_
grid.best_score_

y_pred_train_log = grid.predict(X_train)
y_pred_train = np.exp(y_pred_train_log)
r2_score(y_train, y_pred_train)


y_pred_log = grid.predict(X_test)
y_pred = np.exp(y_pred_log)
r2_score(y_test, y_pred)


## need to hyper parameter tune for SVR model too, I have more paramters to work with.



## HyperParameter Tuning for SVR model

pipe_svr = Pipeline([
    ('processor', processor),
    ('model', SVR())
    
])


param_grid = {
    'model__kernel': ['rbf'],
    'model__C': [0.01,0.1,1,10,50],
    'model__gamma': ['scale',0.001,0.01,0.05],
    'model__epsilon': [0.05,0.1,0.2,0.5]
}

grid_svr = GridSearchCV(
    estimator=pipe_svr,
    param_grid=param_grid,
    scoring='neg_mean_squared_error',
    cv = 5,
    n_jobs= -1,
    verbose=1
)

grid_svr.fit(X_train,y_train_processed)
grid_svr.best_params_
grid_svr.best_score_

y_pred_train_log = grid_svr.predict(X_train)
y_pred_train = np.exp(y_pred_train_log)
r2_score(y_train, y_pred_train)


y_pred_log = grid_svr.predict(X_test)
y_pred = np.exp(y_pred_log)
r2_score(y_test, y_pred)


## the SVR is the better model just by scoring = 'neg_mean_squared_error'
## now we train the best model

grid_svr.best_params_
grid_svr.best_estimator_

pipe_best = Pipeline([
    ('process', processor),
    ('model', SVR(C=10, epsilon=0.2, gamma=0.05, kernel='rbf'))
])

model_log = TransformedTargetRegressor(
    regressor=pipe_best,
    func=np.log,
    inverse_func=np.exp
)


# if we used without TransformedTargetRegressor in our code

# pipe_best.fit(X_train, y_train_processed)
# y_train_pred_log = pipe_best.predict(X_train)
# y_train_pred = np.exp(y_train_pred_log)
# r2_score(y_pred_train_log, y_train_processed)
# # after np.exp()
# r2_score(y_train, y_train_pred)

# r2_score(np.log(y_test), y_pred_log)
#  after np.exp()
# r2_score(y_test, y_pred)

model_log.fit(X_train, y_train) 
y_train_pred = model_log.predict(X_train)

r2_score(y_train, y_train_pred)
root_mean_squared_error(y_train, y_train_pred)


# on test set

y_pred = model_log.predict(X_test)
r2_score(y_test, y_pred)

## Model Eval


residuals = y_test - y_pred

plt.figure(figsize=(7,5))
plt.scatter(y_pred, residuals, alpha=0.6)

plt.axhline(0, color='red', linestyle='--')

plt.xlabel("Predicted price")
plt.ylabel("Residual")
plt.title("SVR Residual Plot")

plt.show()



## making Pipline for RandomForestRegressor Now

pipe_best_n = Pipeline(
    [
        ('processor', processor),
        ('model', RandomForestRegressor())
    ]
)


param_grid_rf = {
    'model__n_estimators': [200, 500, 800],
    'model__max_depth': [5, 10, 20, 30],
    'model__min_samples_split': [5, 10, 20],
    'model__min_samples_leaf': [2, 4, 6, 8],
    'model__max_features': ['sqrt', 'log2', 0.3, 0.5],
    'model__bootstrap': [True],
    'model__max_leaf_nodes': [20, 50, 100],
    'model__ccp_alpha': [0.0, 0.0001, 0.001, 0.01]
}


grid_rf = GridSearchCV(
    estimator=pipe_best_n,
    param_grid=param_grid_rf,
    scoring='neg_mean_squared_error',
    cv = 5,
    n_jobs= -1,
    verbose=1
    
)

grid_rf.fit(X_train, y_train)


grid_rf.best_params_
-grid_rf.best_score_
np.sqrt(-grid_rf.best_score_)


pip = Pipeline(
    [
        ('processor', processor),
        ('model', RandomForestRegressor(bootstrap=True,
                                        max_depth=10,
                                        max_features='sqrt',
                                        min_samples_leaf=1,
                                        min_samples_split=2,
                                        n_estimators=200))
    ]
)



model_log_rf = TransformedTargetRegressor(
    regressor=pip,
    func=np.log,
    inverse_func=np.exp
)

model_log_rf.fit(X_train, y_train)


y_pred_train = model_log_rf.predict(X_train)
r2_score(y_train, y_pred_train)

y_pred = model_log_rf.predict(X_test)
r2_score(y_test, y_pred)


## save the model

joblib_path = "/Users/pouniq/CarPrediction/Deployment/model_dir/SVR_Model.joblib"
dump(model_log, joblib_path)

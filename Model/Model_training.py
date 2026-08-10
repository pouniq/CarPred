import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
import statsmodels.api as sm

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
# OVERFITTING HEAVLY
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



## check the regression model


lr = model_log.regressor_.named_steps["model"]  # fitted LinearRegression
print("Intercept:", lr.intercept_)
print("Coefficients:", lr.coef_)



X_train_proc = processor.fit_transform(X_train)
X_train_sm = sm.add_constant(X_train_proc)

ols_model = sm.OLS(np.log(y_train), X_train_sm).fit()
print(ols_model.summary())


resid = ols_model.resid
fitted = ols_model.fittedvalues

plt.scatter(fitted, resid)

# Drop x3 first (higher p-value = weaker evidence), refit
X_train_no_x3 = np.delete(X_train_proc, 2, axis=1)  # column index 2 = x3
ols_no_x3 = sm.OLS(np.log(y_train), sm.add_constant(X_train_no_x3)).fit()
print(ols_no_x3.summary())


resid = ols_no_x3.resid
fitted = ols_no_x3.fittedvalues

plt.scatter(fitted, resid)


# Now test whether x4 also drops cleanly from this smaller model
X_train_no_x3_x4 = np.delete(X_train_proc, [2, 3], axis=1)
ols_no_x3_x4 = sm.OLS(np.log(y_train), sm.add_constant(X_train_no_x3_x4)).fit()
print(ols_no_x3_x4.summary())

resid = ols_no_x3_x4.resid
fitted = ols_no_x3_x4.fittedvalues

plt.scatter(fitted, resid)


plt.scatter(X_train['insurance'], y_train)

# I found out that deleting X3 and X4 from this 
# linear regression model do not effect the model 
# at all and I can Confidently say that, there is no use
# for `insurance` & `color_2_cat`






# Joint F-test: does removing x3 AND x4 together significantly hurt fit vs. the full model?
f_test = ols_model.compare_f_test(ols_no_x3_x4)
print("F-stat:", f_test[0], "p-value:", f_test[1])
processor.get_feature_names_out()





# we concluded that we the `insurance` and `Color_2_cat` do not have any
# influence to our model at this time.



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

joblib_path = "/Users/pouniq/CarPrediction/Deployment/model_dir/Linear_Model.joblib"
dump(model_log, joblib_path)

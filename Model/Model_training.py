import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

from sklearn.model_selection import GridSearchCV, KFold, cross_val_score
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
    'ridge': Ridge(),
    'svr': SVR(),
    'gbr': GradientBoostingRegressor(max_depth=3, n_estimators=100, random_state=RANDOM_STATE),
    'rfr': RandomForestRegressor(max_depth=5, n_estimators=200, random_state=RANDOM_STATE)
}

for name, est in models.items():
    pipe = Pipeline([('processor', processor), ('model', est)])
    scores = cross_val_score(pipe, X_train, y_train_processed, cv=cv, scoring='r2')
    print(f"{name}: mean R2 = {scores.mean():.3f}, std = {scores.std():.3f}")
    
    
    

print(X_train.shape)
print(np.exp(y_train_processed).describe() if hasattr(y_train_processed, 'describe') else pd.Series(np.exp(y_train_processed)).describe())


###############################################################
###############################################################

?Ridge
# Model Selection Ridge was choosen then SVR, gbr and rfr in order

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


param_grid = [
    {
        'model__kernel': ['rbf'],
        'model__C': [0.1, 1, 10, 100, 1000],
        'model__gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 1],
        'model__epsilon': [0.01, 0.1, 0.2, 0.5]
    },
    {
        'model__kernel': ['linear'],
        'model__C': [0.1, 1, 10, 100],
        'model__epsilon': [0.01, 0.1, 0.2, 0.5]
    },
    {
        'model__kernel': ['poly'],
        'model__C': [0.1, 1, 10, 100],
        'model__degree': [2, 3, 4],
        'model__gamma': ['scale', 'auto'],
        'model__epsilon': [0.01, 0.1, 0.2]
    }
]

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


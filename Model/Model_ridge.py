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


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


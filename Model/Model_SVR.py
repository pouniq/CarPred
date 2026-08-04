## HyperParameter Tuning for SVR model

pipe_svr = Pipeline([
    ('processor', processor),
    ('model', SVR(kernel='rbf'))
    
])

cv = RepeatedKFold(
    n_splits=5,
    n_repeats=10,
    random_state=RANDOM_STATE
)



param_grid = {
    'model__C': [0.1, 1, 10, 50, 100],
    'model__gamma': [
        'scale',
        0.001,
        0.01,
        0.05,
        0.1
    ],
    'model__epsilon': [
        0.01,
        0.05,
        0.1,
        0.2
    ]
}

grid_svr = GridSearchCV(
    pipe_svr,
    param_grid,
    scoring='neg_root_mean_squared_error',
    cv=5,
    n_jobs=-1,
    verbose=1
)

grid_svr.fit(X_train,y_train_processed)
grid_svr.best_params_
-grid_svr.best_score_
# 0.37 --> 0.31

y_pred_train_log = grid_svr.predict(X_train)
y_pred_train = np.exp(y_pred_train_log)
r2_score(y_train, y_pred_train)


y_pred_log = grid_svr.predict(X_test)
y_pred = np.exp(y_pred_log)
r2_score(y_test, y_pred)



best_svr = grid_svr.best_estimator_

scores = cross_val_score(
    best_svr,
    X_train,
    y_train_processed,
    cv= cv,
    scoring="neg_root_mean_squared_error"
)

print(
    -scores.mean(),
    scores.std()
)


scores = cross_val_score(
    best_svr,
    X_train,
    y_train_processed,
    cv=cv,
    scoring="neg_root_mean_squared_error"
)

rmse_scores = -scores

print(rmse_scores)
print("mean:", rmse_scores.mean())
print("std:", rmse_scores.std())


best_svr.fit(X_train, y_train_processed)

train_pred = best_svr.predict(X_train)

train_rmse = root_mean_squared_error(y_train_processed,train_pred)
print(train_rmse)






## the SVR is the better model just by scoring = 'neg_mean_squared_error'
## now we train the best model

grid_svr.best_params_
grid_svr.best_estimator_

pipe_best = Pipeline([
    ('process', processor),
    ('model', SVR(C=10, epsilon=0.01, gamma=0.05, kernel='rbf'))
])

model_log = TransformedTargetRegressor(
    regressor=pipe_best,
    func=np.log,
    inverse_func=np.exp
)


model_log.fit(X_train, y_train)

y_pred_train = model_log.predict(X_train)

errors = pd.DataFrame({
    "actual": y_train,
    "pred": pred,
    "error": abs(y_train - pred)
})

errors.sort_values(
    "error",
    ascending=False
).head(10)


y_pred = model_log.predict(X_test)

train_mape = mean_absolute_percentage_error(y_train, y_pred_train)
test_mape = mean_absolute_percentage_error(y_test, y_pred)


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



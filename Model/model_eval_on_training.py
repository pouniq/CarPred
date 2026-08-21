import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, root_mean_squared_error, mean_squared_error
from joblib import load
from sklearn.model_selection import learning_curve


X_train = pd.read_csv('../PreProcessing/X_train.csv')
X_test = pd.read_csv('../PreProcessing/X_test.csv') 

y_train = pd.read_csv('../PreProcessing/y_train.csv')
y_test = pd.read_csv('../PreProcessing/y_test.csv')


y_train = y_train.values.ravel()
y_test = y_test.values.ravel()


model_lin_reg = load('/Users/pouniq/CarPrediction/Deployment/model_dir/Linear_Model.joblib')

train_sizes, train_scores, valid_scores = learning_curve(
    model_lin_reg,
    X_train,
    y_train,
    train_sizes=np.linspace(0.1, 1.0, 5),
    cv=5,
    scoring="neg_root_mean_squared_error",
)

train_mean = np.median(train_scores, axis=1)
valid_mean = np.median(valid_scores, axis=1)

# 4. Plot the results
plt.figure(figsize=(8, 5))
plt.plot(train_sizes, train_mean, "o-", color="r", label="Training Accuracy")
plt.plot(train_sizes, valid_mean, "o-", color="g", label="Validation Accuracy")

plt.title("Learning Curve: r2 vs. Training Size")
plt.xlabel("Training Set Size")
plt.ylabel("Accuracy")
plt.legend(loc="best")
plt.grid(True)
plt.show()
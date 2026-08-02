import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split



RANDOM_STATE = 42
csv_file = "../Data/CSV/final.csv"
df = pd.read_csv(csv_file)
df = df.drop(columns=['link','price_toman'])


df

train_df = df[0:40]
test_df = df[40:]

train_df.to_csv('train.csv', index=False)
test_df.to_csv('test.csv', index=False)


X = df.drop(columns=['price'])
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=RANDOM_STATE )

# Missing values in `insurance` column

median = X_train['insurance'].median()
X_train['insurance'] = X_train['insurance'].fillna(median)
X_test['insurance'] = X_test['insurance'].fillna(median)


## Handling Outliers 
### no need for Outlier handling at this moment
X_train
X_test

numeric_cols = X_train.columns.drop('color')

for col in numeric_cols:
    plt.boxplot(X_train[col])
    plt.title(f'boxplot for {col}')
    plt.show()

plt.boxplot(np.log(y_train))
plt.boxplot(y_train)
plt.boxplot(y_test)




## encode Categorical Data with OneHotEncoder
numeric_cols = X_train.columns.drop('color')
cat_cols = ['color']


ColProcess = ColumnTransformer([
    ('num', StandardScaler(), numeric_cols),
    ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), cat_cols)
])

X_train_processed = ColProcess.fit_transform(X_train)
X_test_processed = ColProcess.transform(X_test)


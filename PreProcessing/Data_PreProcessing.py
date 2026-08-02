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


X = df[['mileage', 'date', 'insurance', 'color_2_cat']]
y = df['price']

X_train , X_test, y_train, y_test = train_test_split(X, y, random_state=RANDOM_STATE, shuffle=True, test_size=0.2)
X_train.groupby('color_2_cat').count()

# Missing values in `insurance` column

median = X_train['insurance'].median()
X_train['insurance'] = X_train['insurance'].fillna(median)
X_test['insurance'] = X_test['insurance'].fillna(median)



X_train.to_csv('X_train.csv', index=False)
X_test.to_csv('X_test.csv', index=False)


y_train.to_csv('y_train.csv', index=False)
y_test.to_csv('y_test.csv', index = False)

## Handling Outliers 
### no need for Outlier handling at this moment

numeric_cols = ['mileage', 'date', 'insurance']

for col in numeric_cols:
    plt.boxplot(X_train[col])
    plt.title(f'boxplot for {col}')
    plt.show()

plt.boxplot(np.log(y_train))
plt.boxplot(np.log(y_test))
plt.boxplot(y_train)
plt.boxplot(y_test)




import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_link = "../Data/CSV/final.csv"

df = pd.read_csv(df_link)
df = df.drop(columns=['link','price_toman'])


df.shape
df.dtypes
df.info()
df.columns
print(df.nunique())
df.describe().T

# we have 7 missing values in insurance column

num_cols = df.select_dtypes(np.number).columns
cat_cols = df.select_dtypes(str).columns


for col in num_cols:
    plt.figure(figsize=(10,7))
    sns.boxplot(x = df[col])
    plt.title(f'boxplot of {col}')
    plt.show()
    
# some outliers with `price` column


df.duplicated().sum()

df[num_cols].mean()
df[num_cols].var()
df[num_cols].std()



for col in num_cols:
    plt.figure(figsize=(10,7))
    sns.histplot(df[col], kde=True)
    plt.title(f'histogram of {col}')
    plt.show()



    
    
print(df.value_counts())


df.groupby('color').value_counts()

num_cols.corr()
sns.heatmap(num_cols.corr(), cmap = 'coolwarm')
plt.show()



plt.scatter(df['date'], df['mileage'])
plt.xlabel('Date of production')
plt.ylabel('Mileage of the car')
plt.show()



#############Findings###################
# 1. We found in My data that price (targer feature) is not
# in a good place (distribution wise) so I may need to get more data
# or limit and max out my prices to something.

# 2. we have 7 missing values in insurance column
# 3. some outliers with `price` column -- think about how can you handle them

########################################
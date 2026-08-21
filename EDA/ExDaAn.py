import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.float_format', lambda x: f'{x:,.0f}')


df_link = "../Data/CSV/final.csv"

df = pd.read_csv(df_link)
df = df.drop(columns=['link','price_toman', 'color'])
df

df.shape
df.dtypes
df.info()
df.columns
print(df.nunique())
df.describe().T

# we have 20 missing values in insurance column

num_cols = df.select_dtypes(np.number).columns
cat_cols = df.select_dtypes(str).columns


for col in num_cols:
    plt.figure(figsize=(10,7))
    sns.boxplot(x = df[col])
    plt.title(f'boxplot of {col}')
    plt.show()
    
# some outliers with `price` column


mask = df.duplicated()
df[mask]
df = df.drop_duplicates()

df[num_cols].mean()
df[num_cols].var()
df[num_cols].std()


Total_median = df['insurance'].median()
Total_mean = df['insurance'].mean()
df['insurance'] = df['insurance'].fillna(Total_mean)

for col in num_cols:
    plt.figure(figsize=(10,7))
    sns.histplot(df[col], kde=True)
    plt.title(f'histogram of {col}')
    plt.show()



    
    
print(df.value_counts())


df.groupby('color_2_cat').value_counts()

correlations = df[num_cols].corr()
sns.heatmap(correlations, cmap = 'coolwarm', annot=True)
plt.show()



plt.scatter(df['date'], df['mileage'])
plt.xlabel('Date of production')
plt.ylabel('Mileage of the car')
plt.show()



### Bi-Variant EDA:
num_pairs = [
    ('mileage', 'date'),
    ('mileage', 'insurance'),
    ('mileage' , 'price'),
    ('date' , 'insurance'),
    ('date' , 'price'),
    ('insurance' , 'price')
]

for x,y in num_pairs:
   plt.figure(figsize=(5,3)) 
   sns.scatterplot(x = df[x] , y=df[y])
   plt.title(f'{x} vs. {y}')
   plt.xlabel(x)
   plt.ylabel(y)
   plt.show()
   
   
plt.figure(figsize=(5,3))
sns.boxplot(x = df['color_2_cat'] , y= df['price'])
plt.title('Color vs Price boxplot')


df[num_cols].groupby(df['color_2_cat']).count()
df[num_cols].groupby(df['color_2_cat']).mean()
df[num_cols].groupby(df['color_2_cat']).median()


sns.pairplot(df, hue='color_2_cat')
plt.tight_layout()
plt.show()

#############Findings###################
# 1. We found in My data that price (targer feature) is not
# in a good place (distribution wise) so I may need to get more data
# or limit and max out my prices to something.

# 2. we have 7 missing values in insurance column
# 3. some outliers with `price` column -- think about how can you handle them
# 4. Most important features for `price` column is `date` & `mileage`
# 5. I should Drop `color_2_cat` and insurance out of the equations. (it will not work on linear models i know that for sure)
########################################
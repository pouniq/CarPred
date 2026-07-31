import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


plt.rcParams['axes.labelsize'] = 8     # xlabel/ylabel


df_link = "../Data/CSV/final.csv"

df = pd.read_csv(df_link)
df = df.drop(columns=['link','price_toman'])


num_cols = df.select_dtypes(np.number)
cat_cols = df.select_dtypes(str)
df.describe()

print(df.value_counts())


df.groupby('color').value_counts()

num_cols.corr()
sns.heatmap(num_cols.corr(), cmap = 'coolwarm')
plt.show()



plt.scatter(df['date'], df['mileage'])
plt.xlabel('Date of production')
plt.ylabel('Mileage of the car')
plt.show()



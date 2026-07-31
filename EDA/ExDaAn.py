import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_link = "../Data/CSV/final.csv"

df = pd.read_csv(df_link)
df = df.drop(columns=['link','price_toman'])

df.describe()

print(df.value_counts())
plt.bar(df['date'], df['mileage'])
plt.show()



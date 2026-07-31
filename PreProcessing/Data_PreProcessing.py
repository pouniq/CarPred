import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler

csv_file = "../Data/CSV/final.csv"
df = pd.read_csv(csv_file)
df = df.drop(columns=['link','price_toman'])



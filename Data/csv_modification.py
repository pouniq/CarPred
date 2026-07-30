import pandas as pd


data1 = pd.read_csv('CSV/output.csv')
data2 = pd.read_csv('CSV/output1.csv')
lil_data = pd.read_csv("CSV/divar_listings.csv")

# first extract the date of production from the `car` column
# and for cars that do not have them look for that manually
df = pd.concat([data1, data2], ignore_index=True)
# first data loaded to csv

df.to_csv('CSV/final.csv', index=False, encoding='utf-8')
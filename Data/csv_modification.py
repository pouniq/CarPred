import pandas as pd


data1 = pd.read_csv('CSV/output.csv')
data2 = pd.read_csv('CSV/output1.csv')
lil_data = pd.read_csv("CSV/divar_listings.csv")

# first extract the date of production from the `car` column
# and for cars that do not have them look for that manually
df = pd.concat([data1, data2], ignore_index=True)


cols_to_check = [c for c in df.columns if c != "link"]

df.duplicated(subset=cols_to_check).sum()
df = df.drop_duplicates(subset=cols_to_check)

# save to csv
df.to_csv('CSV/final.csv', index=False, encoding='utf-8')
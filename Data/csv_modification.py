import pandas as pd
import re


# data1 = pd.read_csv('CSV/output.csv')
# data2 = pd.read_csv('CSV/output1.csv')
# data3 = pd.read_csv('CSV/output2.csv')
# lil_data = pd.read_csv("CSV/divar_listings.csv")

# data4 = pd.read_csv('CSV/output2.csv')
# data5 = pd.read_csv('CSV/output2.csv')

# first extract the date of production from the `car` column
# and for cars that do not have them look for that manually
# df = pd.concat([data1, data2,data3], ignore_index=True)


df = pd.read_csv("CSV/final.csv")




# persian_digits = "۰۱۲۳۴۵۶۷۸۹"
# translation = str.maketrans(persian_digits, "0123456789")

# def extract_numbers(text):
#     normalized = text.translate(translation)
#     normalized = normalized.replace(",", "").replace("،", "")  # strip both comma types
#     return [int(n) for n in re.findall(r"\d+", normalized)]


# data5["mileage"] = data5["mileage"].apply(lambda x: extract_numbers(x)[0] if extract_numbers(x) else None)
# data5['date'] = data5['date'].apply(lambda x: extract_numbers(x)[0] if extract_numbers(x) else None)

# data5['color'].unique()




# color_rep_two_cat = {
#     'نوک‌مدادی': 'Light',
#     'مشکی' : 'Dark',
#     'سفید': 'Light',
#     'موکا': 'Light',
#     'قهوه‌ای': 'Dark',
#     'طوسی' : 'Light',
#    'نقره‌ای' : 'Light',
#    'خاکستری' : 'Light',
#    'بژ': 'Light',
#    'سرمه‌ای': 'Dark',
#    'زیتونی': 'Light',
#    'Gray' : 'Light',
#    'Black' : 'Dark',
#    'White': 'Light',
#    'Brown': 'Dark',
#    'Olive': 'Light',
#    'Blue': 'Dark'
# }

# data5['color'] = data5['color'].replace(color_rep_two_cat)
# df['color'] = df['color'].replace(color_rep_two_cat)

# df = pd.concat([df, data5], ignore_index=True)


def Convert_date(year):
    year = int(year)
    if year > 1500:
        return year
    else:
       return year + 621

df['date'] = df['date'].apply(Convert_date)

cols_to_check = [c for c in df.columns if c != "link"]

df.duplicated(subset=cols_to_check).sum()
df[df.duplicated(subset=cols_to_check)]

dupes = df[df.duplicated(keep=False)]
print(dupes.sort_values(by=list(df.columns)))
      
df = df.drop_duplicates(subset=cols_to_check)

# to make the color feature more in place
# I made colors that look like each other into one 
# category
df['color'].unique()
# save to csv
df.to_csv('CSV/final.csv', index=False, encoding='utf-8')

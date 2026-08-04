import pandas as pd
import re


# data1 = pd.read_csv('CSV/output.csv')
# data2 = pd.read_csv('CSV/output1.csv')
# data3 = pd.read_csv('CSV/output2.csv')
# lil_data = pd.read_csv("CSV/divar_listings.csv")

# data4 = pd.read_csv('CSV/output2.csv')
data5 = pd.read_csv('CSV/output2.csv')

# first extract the date of production from the `car` column
# and for cars that do not have them look for that manually
# df = pd.concat([data1, data2,data3], ignore_index=True)


df = pd.read_csv("CSV/final.csv")




persian_digits = "۰۱۲۳۴۵۶۷۸۹"
translation = str.maketrans(persian_digits, "0123456789")

def extract_numbers(text):
    normalized = text.translate(translation)
    normalized = normalized.replace(",", "").replace("،", "")  # strip both comma types
    return [int(n) for n in re.findall(r"\d+", normalized)]


data5["mileage"] = data5["mileage"].apply(lambda x: extract_numbers(x)[0] if extract_numbers(x) else None)
data5['date'] = data5['date'].apply(lambda x: extract_numbers(x)[0] if extract_numbers(x) else None)

data5['color'].unique()




color_rep_two_cat = {
    'نوک‌مدادی': 'Dark',
    'مشکی' : 'Dark',
    'سفید': 'Light',
    'موکا': 'Dark',
    'قهوه‌ای': 'Dark',
    'طوسی' : 'Dark',
   'نقره‌ای' : 'Dark',
   'خاکستری' : 'Dark',
   'بژ': 'Light',
   'سرمه‌ای': 'Dark',
   'زیتونی': 'Dark',
   'Gray' : 'Dark',
   'Black' : 'Dark',
   'White': 'Light',
   'Brown': 'Dark',
   'Olive': 'Dark',
   'Blue': 'Dark',
   'آلبالویی': 'Light',
   'زرشکی': 'Dark',
   'سفید صدفی': 'Light',
   'آبی': 'Light',
   'قرمز': 'Light',
   'سایر': 'Light' # I saw the pic it was like light purple
}

data5['color_2_cat'] = data5['color'].replace(color_rep_two_cat)
df['color_2_cat'] = df['color'].replace(color_rep_two_cat)



def Convert_date(year):
    year = int(year)
    if year > 1500:
        return year
    else:
       return year + 621

data5['date'] = data5['date'].apply(Convert_date)

df = pd.concat([df, data5], ignore_index=True)


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

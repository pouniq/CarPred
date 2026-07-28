## I want to scrape a page
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import csv



URL = "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B9/gaoV4rOO?tracker_session_id=dc046025-9565-4d45-8cb6-17a14b385878_gaoV4rOO_N"
response = requests.get(URL)
response.text
soup = BeautifulSoup(response.text, "html.parser")

persian_digits = "۰۱۲۳۴۵۶۷۸۹"
translation = str.maketrans(persian_digits, "0123456789")

cells = [td.get_text(strip=True) for td in soup.find_all("td")]
def extract_numbers(text):
    normalized = text.translate(translation)
    return [int(n) for n in re.findall(r"\d+", normalized)]

cells[0] = extract_numbers(cells[0])
cells[1] = extract_numbers(cells[1])


cells[1] = cells[1][0]
cells[0] = cells[0][0]


# we have more data in here though
kt = soup.select("p.kt-unexpandable-row__value")

insurance = kt[0]
insurance = extract_numbers(insurance.text)[0]

price = kt[3]
price = extract_numbers(price.text)[0]


data_dict = {
    'mileage': cells[0],
    'date': cells[1],
    'color': cells[2],
    'insurance': insurance,
    "price": price,
    'link': URL,
}

pd.DataFrame(data_dict, index=[0])



# now I should work on multiple pages
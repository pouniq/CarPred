import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import csv


URL = "https://divar.ir/s/iran/auto?q=%DA%A9%DB%8C%D8%A7%20%D8%B1%DB%8C%D9%88"

# response = requests.get(URL)
# response.text

# soup = BeautifulSoup(response.text, "html.parser")

# # cars = soup.select("h2.kt-post-card__title")
# # for car in cars:
# #     print(car.text.strip())
# # descr = soup.select("div.kt-post-card__description")


# cards = soup.select("article.kt-post-card")
# mileage = []
# price_list = []
# titles = []
# for card in cards:
#     title_tag = card.select_one("h2.kt-post-card__title")
#     descrip = card.select("div.kt-post-card__description")
    
#     title = title_tag.text.strip() if title_tag else None
#     titles.append(title)
    
#     km = descrip[0].text.strip() if len(descrip) > 0 else None
#     mileage.append(km)
    
#     price = descrip[1].text.strip() if len(descrip) > 1 else None
#     price_list.append(price)
    
#     print(f"{title} with price of {price} have a mileage of {km}")


# cars_data = [
#     {"car": t, "mileage": m, "price": p}
#     for t, m, p in zip(titles, mileage, price_list)
# ]

# with open("cars_scraped.csv", 'w', newline="", encoding="utf-8") as file:
#     writer = csv.DictWriter(file, fieldnames=["car","mileage", "price"])
#     writer.writeheader()
#     writer.writerows(cars_data)
# print("Save to cars_scraped.csv")



## I want to scrape a page

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


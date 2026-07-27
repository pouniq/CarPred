import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv


URL = "https://divar.ir/s/iran/auto?q=%DA%A9%DB%8C%D8%A7%20%D8%B1%DB%8C%D9%88"

response = requests.get(URL)
response.text

soup = BeautifulSoup(response.text, "html.parser")

# cars = soup.select("h2.kt-post-card__title")
# for car in cars:
#     print(car.text.strip())
# descr = soup.select("div.kt-post-card__description")


cards = soup.select("article.kt-post-card")
mileage = []
price_list = []
titles = []
for card in cards:
    title_tag = card.select_one("h2.kt-post-card__title")
    descrip = card.select("div.kt-post-card__description")
    
    title = title_tag.text.strip() if title_tag else None
    titles.append(title)
    
    km = descrip[0].text.strip() if len(descrip) > 0 else None
    mileage.append(km)
    
    price = descrip[1].text.strip() if len(descrip) > 1 else None
    price_list.append(price)
    
    print(f"{title} with price of {price} have a mileage of {km}")


cars_data = [
    {"car": t, "mileage": m, "price": p}
    for t, m, p in zip(titles, mileage, price_list)
]

with open("cars_scraped.csv", 'w', newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["car","mileage", "price"])
    writer.writeheader()
    writer.writerows(cars_data)
print("Save to cars_scraped.csv")






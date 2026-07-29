import requests
from bs4 import BeautifulSoup

URL = 'https://divar.ir/s/iran/car?q=%DA%A9%DB%8C%D8%A7%20%D8%B1%DB%8C%D9%88s'

response = requests.get(URL)
response.text

soup = BeautifulSoup(response.text, "html.parser")
cards_link = soup.select('a.kt-post-card__action')
hrefs = [a["href"] for a in cards_link]
full_links = [f"https://divar.ir{a['href']}" for a in cards_link]

# save the links to txt
with open("links1.txt", 'w', encoding='utf-8') as f:
    f.write("\n".join(full_links))
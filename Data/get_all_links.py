import requests
from bs4 import BeautifulSoup

URL = 'https://divar.ir/s/iran/car?q=%DA%A9%DB%8C%D8%A7%20%D8%B1%DB%8C%D9%88s'

response = requests.get(url=URL, 'html.parser')
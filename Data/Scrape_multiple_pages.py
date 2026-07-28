import time
import random
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd



PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
TRANSLATION = str.maketrans(PERSIAN_DIGITS, "0123456789")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}


def extract_numbers(text):
    normalized = text.translate(TRANSLATION)
    return [int(n) for n in re.findall(r"\d+", normalized)]


def scrape_divar_page(url):
    """Scrape a single Divar listing page and return a dict of fields.
    Returns None if the page couldn't be parsed (missing fields, request error, etc.)."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Request failed for {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    cells = [td.get_text(strip=True) for td in soup.find_all("td")]
    kt = soup.select("p.kt-unexpandable-row__value")

    try:
        mileage = extract_numbers(cells[0])[0]
        date = extract_numbers(cells[1])[0]
        color = cells[2]
        insurance = extract_numbers(kt[0].text)[0]
        price = extract_numbers(kt[3].text)[0]
    except (IndexError, ValueError) as e:
        print(f"[WARN] Could not extract all fields for {url}: {e}")
        return None

    return {
        "mileage": mileage,
        "date": date,
        "color": color,
        "insurance": insurance,
        "price": price,
        "link": url,
    }


def scrape_multiple(urls, delay_range=(2, 5)):
    """Scrape a list of URLs, returning a combined DataFrame.
    delay_range adds a random pause between requests so you don't hammer the server."""
    rows = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Scraping {url}")
        row = scrape_divar_page(url)
        if row:
            rows.append(row)
        # be polite / avoid rate limiting or IP blocks
        if i < len(urls):
            time.sleep(random.uniform(*delay_range))

    return pd.DataFrame(rows)


with open('links.txt', 'r', encoding='utf-8') as f:
    full_links = [line.strip() for line in f if line.strip()]
    


if __name__ == "__main__":
    urls = full_links

    df = scrape_multiple(urls)
    print(df)
    df.to_csv("divar_listings.csv", index=False, encoding="utf-8-sig")
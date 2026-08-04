import time
import random
import re
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright

with open("Links/links1.txt", 'r', encoding='utf-8') as f:
    full_links = [line.strip() for line in f if line.strip()]

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

persian_digits = "۰۱۲۳۴۵۶۷۸۹"
translation = str.maketrans(persian_digits, "0123456789")

def extract_numbers(text):
    normalized = text.translate(translation)
    normalized = normalized.replace(",", "").replace("،", "")  # strip both comma types
    return [int(n) for n in re.findall(r"\d+", normalized)]



full_links1 =[
    
    
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-90/gaxtYHq6?tracker_session_id=69cc556e-9617-4961-bd55-1ac8a4fc8f9a_gaxtYHq6_N",
    "https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B9-%D8%B3%D8%A7%D9%84%D9%85-%D9%88-%D8%A2%D9%85%D8%A7%D8%AF%D9%87-%D8%A8%D9%87-%DA%A9%D8%A7%D8%B1/gabpay8a?tracker_session_id=69cc556e-9617-4961-bd55-1ac8a4fc8f9a_gabpay8a_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D8%B3%D9%88%D8%A7%D8%B1%DB%8C-%D9%85%D8%AF%D9%84%DB%B8%DB%B8%D8%B3%D9%81%DB%8C%D8%AF/gaxRJy6K?tracker_session_id=69cc556e-9617-4961-bd55-1ac8a4fc8f9a_gaxRJy6K_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B5/gaxNJWoP?tracker_session_id=69cc556e-9617-4961-bd55-1ac8a4fc8f9a_gaxNJWoP_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%DB%B8%DB%B7/gaxFqUqg?tracker_session_id=69cc556e-9617-4961-bd55-1ac8a4fc8f9a_gaxFqUqg_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%DB%B8%DB%B8-%DA%A9%D9%85-%DA%A9%D8%A7%D8%B1-%D9%88%D8%A7%D9%82%D8%B9%DB%8C/gaxRo-cC?tracker_session_id=69cc556e-9617-4961-bd55-1ac8a4fc8f9a_gaxRo-cC_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B9-%D8%A8%D8%AF%D9%88%D9%86-%D8%B1%D9%86%DA%AF/gaxN41tv?tracker_session_id=69cc556e-9617-4961-bd55-1ac8a4fc8f9a_gaxN41tv_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B5-%D8%AF%D8%B1%D8%AD%D8%AF-%D8%A8%D8%AF%D9%88%D9%86-%D9%85%D8%B4%D8%A7%D8%A8%D9%87/gaxl4ire?tracker_session_id=69cc556e-9617-4961-bd55-1ac8a4fc8f9a_gaxl4ire_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-90-abs-%D8%A8%DB%8C-%D9%87%D8%B2%DB%8C%D9%86%D9%87/gahlsLDj?tracker_session_id=69cc556e-9617-4961-bd55-1ac8a4fc8f9a_gahlsLDj_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84%DB%B9%DB%B0/gaxhYhUX?tracker_session_id=69cc556e-9617-4961-bd55-1ac8a4fc8f9a_gaxhYhUX_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88%D9%85%D8%AF%D9%84%DB%B8%DB%B5/gaxFoz0V?tracker_session_id=69cc556e-9617-4961-bd55-1ac8a4fc8f9a_gaxFoz0V_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%87%D8%A7%DA%86%D8%A8%DA%A9-2015-%D9%86%D9%88%DA%A9-%D9%85%D8%AF%D8%A7%D8%AF%DB%8C-%D8%A8%DB%8C-%D8%B1%D9%86%DA%AF/gaLxGVUm?tracker_session_id=69cc556e-9617-4961-bd55-1ac8a4fc8f9a_gaLxGVUm_N"
    
]




pages = {}
failed_debug_dir = "failed_pages"
import os
os.makedirs(failed_debug_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome")
    context = browser.new_context(user_agent=USER_AGENT, locale="fa-IR")
    page = context.new_page()

    for i, url in enumerate(full_links1):
        success = False
        for attempt in range(3):  # retry up to 3 times
            try:
                response = page.goto(url, timeout=20000, wait_until="domcontentloaded")

                # Wait specifically for the data table to show up, not just DOMContentLoaded
                page.wait_for_selector("table.kt-group-row", timeout=8000)

                html = page.content()
                pages[url] = html
                success = True
                break
            except Exception as e:
                print(f"[{i}] attempt {attempt+1} failed for {url}: {e}")
                time.sleep(random.uniform(4, 8))  # back off longer on failure

        if not success:
            # Save whatever we got, for inspection
            try:
                html = page.content()
                with open(f"{failed_debug_dir}/{i}.html", "w", encoding="utf-8") as f:
                    f.write(html)
            except Exception:
                pass
            print(f"[{i}] giving up on {url}")

        time.sleep(random.uniform(2, 5))

    browser.close()

# --- Parsing stays the same ---
results = []
for url, html in pages.items():
    soup = BeautifulSoup(html, "html.parser")
    cells = [td.get_text(strip=True) for td in soup.select(
        "td.kt-group-row-item.kt-group-row-item__value.kt-group-row-item--info-row"
    )]
    kt = soup.select("p.kt-unexpandable-row__value")

    try:
        insurance = extract_numbers(kt[0].get_text())[0]
        price = extract_numbers(kt[3].get_text())[0]
    except (IndexError, ValueError):
        insurance, price = None, None

    results.append({
        'mileage': cells[0] if len(cells) > 0 else None,
        'date': cells[1] if len(cells) > 1 else None,
        'color': cells[2] if len(cells) > 2 else None,
        'insurance': insurance,
        'price': price,
        'link': url,
    })

df = pd.DataFrame(results)
df['price'] = df['price'].astype('Int64')       # nullable integer, keeps NaN as <NA>
df['insurance'] = df['insurance'].astype('Int64')
df['price_toman'] = df['price'].apply(lambda x: f"{x:,} تومان" if pd.notna(x) else None)

df.to_csv("CSV/output2.csv", index=False, encoding="utf-8-sig")
print(df)
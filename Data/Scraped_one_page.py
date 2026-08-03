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
    
    
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-89/gawZ1kxK?tracker_session_id=8cecef3f-2d68-4f4d-8e23-5bfb7f67dc6b_gawZ1kxK_N",
"https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88-%D9%87%D8%A7%DA%86-%D8%A8%DA%A9-%DB%B2%DB%B0%DB%B1%DB%B5-%D8%AE%D9%84%DB%8C%D8%AC/gaodbaim?tracker_session_id=2cbf53ea-719b-4a56-8251-0d49c5efec52_gaodbaim_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%DB%B8%DB%B6/gawJ1NZr?tracker_session_id=9c7bb739-0fc9-4e93-a07a-ded6f79447e4_gawJ1NZr_N",
"https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88-%DB%B2%DB%B0%DB%B1%DB%B6/gaw90jsg?tracker_session_id=c99467cd-dd5a-4d26-b5eb-cd081874582e_gaw90jsg_N",
"https://divar.ir/v/%D9%81%D8%B1%D9%88%D8%B4-%D8%AE%D9%88%D8%AF%D8%B1%D9%88/gaw1Ukdy?tracker_session_id=5b131e93-fcfd-45d5-9274-e06b2b73c98b_gaw1Ukdy_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B8-%D8%A8%DB%8C-%D8%B1%D9%86%DA%AF/gavBQelw?tracker_session_id=d6b758d3-458a-4c2c-ae89-d43e3a2a450c_gavBQelw_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-87-%D8%AA%D9%85%DB%8C%D8%B2/gawpUANF?tracker_session_id=cec3a494-b7ca-46c3-a0a6-5c6ee26ca149_gawpUANF_N",
"https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B1%DB%B3%DB%B9%DB%B0/gawlknoQ?tracker_session_id=25265d55-f99d-4f34-b981-4200dd744710_gawlknoQ_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B9/gawhED31?tracker_session_id=63f742a6-55c2-42ed-ac7a-9344afeaa4ea_gawhED31_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%DB%B8%DB%B9-%D8%A7%D8%B3%D8%AA%D8%AB%D9%86%D8%A7%DB%8C%DB%8C-%DB%B1%DB%B0%DB%B0-%D8%AA%D8%A7-%DA%A9%D8%A7%D8%B1/gawh0V0Z?tracker_session_id=b1cfd3f5-7f4e-4778-b7f3-d70094546519_gawh0V0Z_N"

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
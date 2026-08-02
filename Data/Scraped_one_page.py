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



full_links1 = ["https://divar.ir/v/%D9%81%D8%B1%D9%88%D8%B4-%D8%B1%DB%8C%D9%88-%D8%AE%D8%A7%D9%86%DA%AF%DB%8C-%D9%88-%D8%B3%D8%A7%D9%84%D9%85/gajtM-Iy?tracker_session_id=958f285d-d693-4c47-9414-b552f37f3ef2_gajtM-Iy_P",
                "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-87/gauZ__fJ?tracker_session_id=b73e4f38-f74f-4e9d-992b-170c875de2a0_gauZ__fJ_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D8%A7%D8%AA%D9%88%D9%85%D8%A7%D8%AA%DB%8C%DA%A9-%DA%A9%D8%A7%D8%B1%D8%AE%D8%A7%D9%86%D9%87/gabJWd2i?tracker_session_id=3b80ad50-9541-43af-94c5-c1ac820cb947_gabJWd2i_P",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84%DB%B8%DB%B9-%D8%AA%D9%85%DB%8C%D8%B2-%D8%AE%D8%A7%D9%86%DA%AF%DB%8C-%D8%B3%D8%A7%D9%84%D9%85/gauV_np5?tracker_session_id=81dd1e8a-cee8-48aa-bef5-3bfb4af29163_gauV_np5_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-88/gaoBImRD?tracker_session_id=34c48c2c-b578-4537-89f8-ac0518826024_gaoBImRD_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-87-%D9%86%D9%88%DA%A9-%D9%85%D8%AF%D8%A7%D8%AF%DB%8C/gau5eWng?tracker_session_id=99ad18b9-fe07-449a-8333-9166f94642b8_gau5eWng_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88%DB%B8%DB%B5/gauxe96w?tracker_session_id=c30f71cc-3fb3-4539-8a53-d124348b195e_gauxe96w_N"
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%DB%B8%DB%B6-%D8%A8%D8%AF%D9%88%D9%86-%D8%B1%D9%86%DA%AF-%D8%AA%D9%85%DB%8C%D8%B2/gaudug2R?tracker_session_id=4846e4ea-b673-409e-bb9b-85c576b593eb_gaudug2R_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B9%DB%B0/gauJ-sxR?tracker_session_id=a1153f8d-0edb-4562-9dbb-8d3cd41cf28c_gauJ-sxR_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D8%B2%DB%8C%D8%AA%D9%88%D9%86%DB%8C-%D9%85%D8%AF%D9%84-%DB%B8%DB%B6/gau5Nkal?tracker_session_id=5c5262b7-5912-44a0-abf1-c7161f252dac_gau5Nkal_N]"]
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
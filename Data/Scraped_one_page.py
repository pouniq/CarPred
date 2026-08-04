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
    
    
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B9%DB%B1-%D8%A7%D8%B3%D8%AA%D8%AB%D9%86%D8%A7%DB%8C%DB%8C/gaxR_wYi?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxR_wYi_N",   
"https://divar.ir/v/%D8%AE%D9%88%D8%AF%D8%B1%D9%88-%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84%DB%B8%DB%B9/gaxNPbPO?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxNPbPO_N",   
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B9%DB%B0/gaxFPaxr?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxFPaxr_N",   
"https://divar.ir/v/%D9%81%D8%B1%D9%88%D8%B4-%D9%85%D8%A7%D8%B4%DB%8C%D9%86-%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B5/gaxBPdWc?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxBPdWc_N",   
"https://divar.ir/v/%D8%B1%DB%8C%D9%88%D9%85%D8%AF%D9%84%DB%B9%DB%B0/gax5Obvd?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gax5Obvd_N",   
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B7/gaBF5fU-?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaBF5fU-_N",   
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-1385/gaxVOVZE?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxVOVZE_N",   
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B9%DB%B0/gaxJel09?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxJel09_N",   
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-89/gaxBu5vc?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxBu5vc_N",   
"https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88/gax59FMz?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gax59FMz_N",   
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B5/gaxx98W4?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxx98W4_N",   
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%B4%DA%A9%DB%8C-%D9%85%D8%AA%D8%A7%D9%84%DB%8C%DA%A9-%D8%B3%D8%B1%D9%BE%D8%A7/gaU5ckHp?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaU5ckHp_N",   
"https://divar.ir/v/%D9%85%D8%A7%D8%B4%DB%8C%D9%86-%D8%B1%DB%8C%D9%88/gaxp96WY?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxp96WY_N",   
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-89/gaxpd-N0?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxpd-N0_N",   
"https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88-2015%D9%81%D9%82%D8%B7-%DB%B6%DB%B0%DA%A9%D8%A7%D8%B1/gaxZbHmG?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxZbHmG_N",   
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B7/gaxNNJGL?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxNNJGL_N",   
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%DB%B8%DB%B4-%D9%86%D9%88%DA%A9-%D9%85%D8%AF%D8%A7%D8%AF%DB%8C/gam9ylHw?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gam9ylHw_N",   
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B8-%D8%AA%D9%85%DB%8C%D8%B2-%D9%88-%D8%B3%D9%84%D8%A7%D9%85%D8%AA/gaxFNfji?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxFNfji_N",   
"https://divar.ir/v/%D8%B1%DB%8C%D9%88/gax1sLfV?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gax1sLfV_N",
"https://divar.ir/v/%DB%8C%DA%A9-%D8%B1%DB%8C%D9%88%DB%8C-%D8%AE%D8%A7%D8%B5/ganFUKvf?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_ganFUKvf_N",
"https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88-%D9%85%D9%88%D9%86%D8%AA%D8%A7%DA%98-%D8%AF%D9%86%D8%AF%D9%87-%DB%B8%DB%B9-%D8%A8%DB%8C%D8%B1%D9%86%DA%AF/gaxlcC6N?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxlcC6N_N",
"https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-90/gaxRMXe_?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxRMXe__N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D9%85%D8%AF%D9%84/gaxBcIpC?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxBcIpC_N",
"https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88-%D9%87%D8%A7%DA%86-%D8%A8%DA%A9-%DB%B2%DB%B0%DB%B1%DB%B6/gax9r_zm?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gax9r_zm_N",
"https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88-%DB%B2%DB%B0%DB%B1%DB%B6/gax5rlW-?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gax5rlW-_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%DB%B2%DB%B0%DB%B1%DB%B6-%D9%81%D9%88%D9%84-%D8%A8%D8%AF%D9%88%D9%86-%D8%B1%D9%86%DA%AF/gafpWT65?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gafpWT65_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88/gaxJM3Xb?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxJM3Xb_N",
"https://divar.ir/v/%DA%A9%DB%8C%D8%A7%D8%B1%DB%8C%D9%88-%D8%B5%D9%86%D8%AF%D9%88%D9%82%D8%AF%D8%A7%D8%B1%DB%B2%DB%B0%DB%B1%DB%B5%D9%81%D9%88%D9%84-%D8%AE%D9%84%DB%8C%D8%AC-%D9%84%D8%A7%DA%A9%D8%A7%D8%BA%D8%B0%DB%8C/gaxdC4HS?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxdC4HS_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-89-%D8%B9%D8%B1%D9%88%D8%B3%DA%A9/ganhEUrV?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_ganhEUrV_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-87-%D8%AF%D8%B1-%D8%AD%D8%AF/gantGAQF?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gantGAQF_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B7/gax5K1A-?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gax5K1A-_N",
"https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B2%DB%B0%DB%B1%DB%B5-%D8%B3%D9%81%D8%A7%D8%B1%D8%B4-%D8%AE%D9%84%DB%8C%D8%AC-%D8%A8%D8%AF%D9%88%D9%86-%D8%B1%D9%86%DA%AF/gaxt5ObE?tracker_session_id=ea124b22-09ff-49c0-94a9-4544d7370d76_gaxt5ObE_N",

   
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
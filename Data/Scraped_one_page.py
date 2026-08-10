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
    
    
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D9%88%D9%86%D8%AA%D8%A7%DA%98-%DA%A9%D9%85-%DA%A9%D8%A7%D8%B1-%D8%AE%D8%A7%D9%86%DA%AF%DB%8C/ga6RCd1z?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga6RCd1z_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%DA%A9%D8%A7%D9%85%D9%84%D8%A7-%D8%B3%D8%A7%D9%84%D9%85/gaaFXYzB?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_gaaFXYzB_N",
    
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B9%DB%B0/ga6BCH3o?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga6BCH3o_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D8%AF%D8%B1%D8%AC%D9%87-%DB%8C%DA%A9/gaWNL4dM?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_gaWNL4dM_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-89-%D8%AE%D8%A7%D9%86%DA%AF%DB%8C/ga61ByMV?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga61ByMV_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B6/ga6lRDyX?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga6lRDyX_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B9%DB%B0/ga6VRIg6?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga6VRIg6_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D8%AA%DA%A9-%D8%A8%D8%B1%DA%AF-%D8%B3%D9%86%D8%AF-%D8%A2%D8%AE%D8%B1-%DB%B8%DB%B8/ga61gKmp?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga61gKmp_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D8%AE%D8%A7%D9%86%DA%AF%DB%8C-%D8%AF%D8%B1%D8%AC%D9%87-1/ga4RKQOk?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga4RKQOk_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%DB%B8%DB%B5/ga4JZ1TE?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga4JZ1TE_N",
    "https://divar.ir/v/%D8%AE%D9%88%D8%AF%D8%B1%D9%88-%D8%B1%DB%8C%D9%88-%D8%B3%D8%AF%D8%A7%D9%86-%D8%A7%D8%B1%D9%88%D9%86%D8%AF%DB%8C/ga4p1Qcj?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga4p1Qcj_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B1%DB%B3%DB%B8%DB%B9/gavxIM_q?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_gavxIM_q_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B9/ga2pOaqn?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga2pOaqn_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B8-%D8%AA%D9%85%DB%8C%D8%B2-%D9%88-%D8%B3%D9%84%D8%A7%D9%85%D8%AA/gaxFNfji?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_gaxFNfji_N",
    "https://divar.ir/v/%D9%81%D8%B1%D9%88%D8%B4-%D8%AE%D9%88%D8%AF%D8%B1%D9%88-%D8%B1%DB%8C%D9%88-%DA%A9%DB%8C%D8%A7/ga4dTvzb?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga4dTvzb_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88%DB%B2%DB%B0%DB%B1%DB%B4/ga4dzchF?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga4dzchF_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-88%D8%A8%D8%AF%D9%88%D9%86-%D8%B1%D9%86%DA%AF-%D9%88%D8%B3%D9%85%D9%86%D8%AF92/ga4VzMAn?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga4VzMAn_N",
    "https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88-2015%D8%AE%D9%84%DB%8C%D8%AC-%D8%B3%D8%A7%D9%86%D8%B1%D9%88%D9%81-%D8%A8%D8%AF%D9%88%D9%86-%D8%B1%D9%86%DA%AF/ga4lyVoc?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga4lyVoc_N",
    "https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88-%D8%AF%D9%86%D8%AF%D9%87-%D9%85%D9%88%D9%86%D8%AA%D8%A7%DA%98-%DB%B8%DB%B9-%D8%A8%DB%8C%D8%B1%D9%86%DA%AF/ga2Nu1eq?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga2Nu1eq_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B9-%D8%A8%D8%AF%D9%88%D9%86-%D8%B1%D9%86%DA%AF/ga4Nx9QF?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga4Nx9QF_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%DB%B8%DB%B6/ga4tR8zk?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga4tR8zk_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B7/ga4VhZa7?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga4VhZa7_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B6-%DA%A9%D8%B1%D9%87-%D8%A7%DB%8C-%D9%81%D8%A7%D8%A8%D8%B1%DB%8C%DA%A9-%D8%A7%D8%B3%D8%AA%D8%AB%D9%86%D8%A7%DB%8C%DB%8C/ga4NRHsx?tracker_session_id=64c2de26-ef81-47b9-8b67-eb834830247a_ga4NRHsx_N",
    "https://divar.ir/v/%D9%81%D8%B1%D9%88%D8%B4-%D8%B1%DB%8C%D9%88-%DB%B2%DB%B0%DB%B1%DB%B6-%D9%81%D9%88%D9%84-%D8%A8%D8%AF%D9%88%D9%86-%D8%B1%D9%86%DA%AF-%DA%A9%D9%85-%DA%A9%D8%A7%D8%B1/ga59FU5B?tracker_session_id=387891fd-3488-40d2-ab15-fcd552d0e0cc_ga59FU5B_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B9-%D9%86%D9%82%D8%AF-%D9%88-%D8%A7%D9%82%D8%B3%D8%A7%D8%B7/gaftRY0w?tracker_session_id=387891fd-3488-40d2-ab15-fcd552d0e0cc_gaftRY0w_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D8%A7%D8%AA%D9%88%D9%85%D8%A7%D8%AA/gajF8iTu?tracker_session_id=387891fd-3488-40d2-ab15-fcd552d0e0cc_gajF8iTu_N",
    "https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88/gap949qY?tracker_session_id=387891fd-3488-40d2-ab15-fcd552d0e0cc_gap949qY_N",
    "https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88-%D9%88%D8%A7%D8%B1%D8%AF%D8%A7%D8%AA%DB%8C-%DB%B2%DB%B0%DB%B1%DB%B5%D9%81%D9%86%DB%8C-%D8%B3%D8%B1%D8%AD%D8%A7%D9%84-%D8%B4%D8%A7%D8%B3%DB%8C-%D9%88-%D8%B3%D8%AA%D9%88%D9%86-%D9%87%D8%A7-%D8%B3%D8%A7%D9%84%D9%85/gawRZsNt?tracker_session_id=387891fd-3488-40d2-ab15-fcd552d0e0cc_gawRZsNt_N",
    "https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%DB%B2%DB%B0%DB%B1%DB%B4-%D9%86%DB%8C%D9%85%D9%87-%D9%81%D9%88%D9%84-%D8%A7%D8%B1%D9%88%D9%86%D8%AF%DB%8C/gaxpKx75?tracker_session_id=387891fd-3488-40d2-ab15-fcd552d0e0cc_gaxpKx75_N",
    "https://divar.ir/v/%DA%A9%DB%8C%D8%A7-%D8%B1%DB%8C%D9%88-%D8%B3%D8%AF%D8%A7%D9%86-%DB%B2%DB%B0%DB%B1%DB%B5-%D9%BE%D9%84%D8%A7%DA%A9-%D8%AB%D8%A7%D8%A8%D8%AA-%D9%85%D9%86%D8%B7%D9%82%D9%87/gay5g_Wf?tracker_session_id=387891fd-3488-40d2-ab15-fcd552d0e0cc_gay5g_Wf_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%DB%B8%DB%B9/galt8oia?tracker_session_id=387891fd-3488-40d2-ab15-fcd552d0e0cc_galt8oia_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88%DB%B2%DB%B0%DB%B1%DB%B4/ga4dzchF?tracker_session_id=387891fd-3488-40d2-ab15-fcd552d0e0cc_ga4dzchF_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D9%88%D9%86%D8%AA%D8%A7%DA%98-%D9%85%D8%AF%D9%84-%DB%B8%DB%B7/gavd5DFj?tracker_session_id=387891fd-3488-40d2-ab15-fcd552d0e0cc_gavd5DFj_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B9%DB%B0/ga4ViMx_?tracker_session_id=387891fd-3488-40d2-ab15-fcd552d0e0cc_ga4ViMx__N",
    "https://divar.ir/v/%D9%81%D8%B1%D9%88%D8%B4/ga4BBo29?tracker_session_id=387891fd-3488-40d2-ab15-fcd552d0e0cc_ga4BBo29_N",
    "https://divar.ir/v/%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-%DB%B8%DB%B8/ga4JzkCu?tracker_session_id=387891fd-3488-40d2-ab15-fcd552d0e0cc_ga4JzkCu_N"

]

len(full_links1)

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
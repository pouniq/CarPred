from playwright.sync_api import sync_playwright

URL = "https://divar.ir/s/tehran/car/kia/rio"


def get_links(url: str) -> list[str]:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome",headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        # wait for at least one result card to show up before scraping
        page.wait_for_selector("a.kt-post-card__action", timeout=15000)

        hrefs = page.eval_on_selector_all(
            "a.kt-post-card__action",
            "elements => elements.map(el => el.getAttribute('href'))",
        )

        browser.close()

    full_links = [f"https://divar.ir{href}" for href in hrefs if href]
    return full_links


if __name__ == "__main__":
    links = get_links(URL)

    with open("links1.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(links))

    print(f"Saved {len(links)} links to links1.txt")


def get_links(url: str) -> list[str]:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome",headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        # wait for at least one result card to show up before scraping
        page.wait_for_selector("a.kt-post-card__action", timeout=15000)

        hrefs = page.eval_on_selector_all(
            "a.kt-post-card__action",
            "elements => elements.map(el => el.getAttribute('href'))",
        )

        browser.close()

    full_links = [f"https://divar.ir{href}" for href in hrefs if href]
    return full_links


if __name__ == "__main__":
    links = get_links(URL)

    with open("links1.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(links))

    print(f"Saved {len(links)} links to links1.txt")
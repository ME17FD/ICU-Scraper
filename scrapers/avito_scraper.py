import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.export import export_data
from utils.helpers import fetch_soup, safe_text_extract, safe_attribute_extract, make_absolute_url, rate_limit


BASE_URL = "https://www.avito.ma"
HEADERS = {"User-Agent": "Mozilla/5.0"}





def parse_card(card, fields):
    try:
        data = {}
        if "link" in fields:
            a_tag = card if card.name == "a" else card.find("a", class_="sc-1jge648-0")
            href = safe_attribute_extract(a_tag, "href") if a_tag else "N/A"
            data["link"] = make_absolute_url(href, BASE_URL)

        if "title" in fields:
            tag = card.select_one("p[title]")
            data["title"] = safe_attribute_extract(tag, "title")

        if "price" in fields:
            tag = card.select_one("p.sc-b57yxx-3")
            data["price"] = safe_text_extract(tag).replace("\u202f", "")

        if "location" in fields:
            tag = card.select_one("div.sc-b57yxx-11 p")
            data["location"] = safe_text_extract(tag)

        if "details" in fields:
            spans = [span.get_text(strip=True) for span in card.select("div.sc-b57yxx-2 span span")]
            data["details"] = ", ".join(filter(None, spans)) or "N/A"

        if "seller" in fields:
            tag = card.select_one("p.sc-1wnmz4-5")
            data["seller"] = safe_text_extract(tag)

        if "date" in fields:
            tag = card.select_one("div.sc-1wnmz4-2 p")
            data["date"] = safe_text_extract(tag)

        if "image" in fields:
            tag = card.select_one("div.sc-bsm2tm-2 img")
            data["image"] = safe_attribute_extract(tag, "src")

        return data
    except Exception as e:
        print("❌ Error parsing:", e)
        return None


def scrape_avito(url, pages=1, delay=1, fields=None):
    if fields is None:
        fields = {"title", "price", "location", "details", "link", "seller", "date", "image"}

    results = []
    for page in range(1, pages + 1):
        page_url = f"{url}?o={page}"
        print(f"🔎 Scraping page {page}: {page_url}")
        soup = fetch_soup(page_url, headers=HEADERS)
        if not soup:
            break

        cards = soup.select("a.sc-1jge648-0")
        for card in cards:
            data = parse_card(card, fields)
            if data:
                results.append(data)
        rate_limit(delay)

    return results, fields





# === MAIN SCRIPT ===
if __name__ == "__main__":
    # 🛠️ Customize these:
    url = "https://www.avito.ma/fr/maroc/appartement_casablanca"
    pages = 3
    fields = None  # Or set like {"title", "price", "link", "image"}
    fmt = "xlsx"   # "csv" or "xlsx"

    results, used_fields = scrape_avito(url, pages=pages, fields=fields)
    export_data(results, list(used_fields), url, pages, fmt, site_name="avito_ma")

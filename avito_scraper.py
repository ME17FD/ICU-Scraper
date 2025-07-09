import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse


BASE_URL = "https://www.avito.ma"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_soup(url):
    try:
        res = requests.get(url, headers=HEADERS)
        if res.status_code == 200:
            return BeautifulSoup(res.content, "html.parser")
        else:
            print(f"⚠️ Error {res.status_code}: {url}")
            return None
    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return None


def parse_card(card, fields):
    try:
        data = {}
        if "link" in fields:
            a_tag = card if card.name == "a" else card.find("a", class_="sc-1jge648-0")
            data["link"] = urljoin(BASE_URL, a_tag.get("href")) if a_tag else "N/A"

        if "title" in fields:
            tag = card.select_one("p[title]")
            data["title"] = tag.get("title") if tag else "N/A"

        if "price" in fields:
            tag = card.select_one("p.sc-b57yxx-3")
            data["price"] = tag.text.strip().replace("\u202f", "") if tag else "N/A"

        if "location" in fields:
            tag = card.select_one("div.sc-b57yxx-11 p")
            data["location"] = tag.text.strip() if tag else "N/A"

        if "details" in fields:
            spans = [span.get_text(strip=True) for span in card.select("div.sc-b57yxx-2 span span")]
            data["details"] = ", ".join(filter(None, spans)) or "N/A"

        if "seller" in fields:
            tag = card.select_one("p.sc-1wnmz4-5")
            data["seller"] = tag.text.strip() if tag else "N/A"

        if "date" in fields:
            tag = card.select_one("div.sc-1wnmz4-2 p")
            data["date"] = tag.text.strip() if tag else "N/A"

        if "image" in fields:
            tag = card.select_one("div.sc-bsm2tm-2 img")
            data["image"] = tag.get("src") if tag else "N/A"

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
        soup = fetch_soup(page_url)
        if not soup:
            break

        cards = soup.select("a.sc-1jge648-0")
        for card in cards:
            data = parse_card(card, fields)
            if data:
                results.append(data)
        time.sleep(delay)

    return results, fields


def export_data(data, fields, url, pages_scraped, output_format="xlsx"):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    base_name = url.split("/")[-1].split("?")[0] or "avito_results"
    filename = f"{base_name}_{now}.{output_format}"

    doc_string = (
        f"Avito Scraper Summary\n"
        f"- URL: {url}\n"
        f"- Pages Scraped: {pages_scraped}\n"
        f"- Fields: {', '.join(fields)}\n"
        f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"- Total items: {len(data)}"
    )

    df = pd.DataFrame(data)

    if output_format == "csv":
        # Add documentation as commented lines
        with open(filename, "w", encoding="utf-8") as f:
            for line in doc_string.splitlines():
                f.write(f"# {line}\n")
            df.to_csv(f, index=False)
    else:
        # Write to Excel with 2 sheets
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            # Sheet 1: Data
            df.to_excel(writer, sheet_name="Listings", index=False)

            # Sheet 2: Metadata
            meta_df = pd.DataFrame({
                "Info": doc_string.splitlines()
            })
            meta_df.to_excel(writer, sheet_name="Documentation", index=False)

    print(f"✅ Exported to {filename}")


# === MAIN SCRIPT ===
if __name__ == "__main__":
    # 🛠️ Customize these:
    url = "https://www.avito.ma/fr/maroc/appartement_casablanca"
    pages = 3
    fields = None  # Or set like {"title", "price", "link", "image"}
    fmt = "xlsx"   # "csv" or "xlsx"

    results, used_fields = scrape_avito(url, pages=pages, fields=fields)
    export_data(results, used_fields, url, pages, fmt)

import requests
from bs4 import BeautifulSoup
import os
import time
import re
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.export import export_category_data
from utils.helpers import fetch_soup, safe_text_extract, safe_attribute_extract, ensure_directory, download_image, rate_limit, slugify

# --- CONFIG ---
BASE_URL = "https://1moment.ma"
CATEGORIES = [
    "make-up",
    "maman-bebe",
    "parfum",
    "idees-cadeaux",
    "complement-alimentaire-et-force",
    "accessoires",
    "parapharmacie"
]
IMAGE_FOLDER = "product_images"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Make image folder
ensure_directory(IMAGE_FOLDER)

def scrape_category(category, save_images=True, delay=1):
    print(f"\n📂 Scraping category: {category}")
    category_url_base = f"{BASE_URL}/categorie/{category}/page/"
    products_data = []
    page = 1

    while True:
        print(f"🔄 Page {page}")
        page_url = f"{category_url_base}{page}/"
        soup = fetch_soup(page_url, headers=HEADERS)

        if not soup:
            print(f"❌ Page {page} not found, stopping.")
            break
        product_elements = soup.select("li.product")

        if not product_elements:
            print(f"✅ No products on page {page}, stopping.")
            break

        for product_div in product_elements:
            caption = product_div.select_one("div.caption")
            if not caption:
                continue

            # --- Product Title & Link ---
            title_tag = caption.select_one("h3.woocommerce-loop-product__title a")
            title = safe_text_extract(title_tag)
            product_link = safe_attribute_extract(title_tag, "href")

            # --- Default values ---
            photo_url = ""
            image_filename = ""
            price_new = ""
            price_old = ""
            description = ""

            # --- Image from category ---
            img_tag = product_div.select_one("img")
            photo_url = safe_attribute_extract(img_tag, "src")

            # --- Price ---
            price_container = caption.select_one("span.price")
            if price_container:
                new_price_tag = price_container.select_one("ins bdi")
                if new_price_tag:
                    price_new = new_price_tag.text.strip().replace('\xa0', ' ')
                else:
                    bdi_tag = price_container.select_one("bdi")
                    if bdi_tag:
                        price_new = bdi_tag.text.strip().replace('\xa0', ' ')
                old_price_tag = price_container.select_one("del bdi")
                if old_price_tag:
                    price_old = old_price_tag.text.strip().replace('\xa0', ' ')

            # --- Categories ---
            categories = ", ".join(a.text.strip() for a in caption.select("div.posted_in a"))

            # --- Product page (description & fallback image) ---
            if product_link:
                try:
                    prod_soup = fetch_soup(product_link, headers=HEADERS)

                    # Description
                    desc_tag = prod_soup.select_one("div.woocommerce-Tabs-panel--description p")
                    description = safe_text_extract(desc_tag)

                    # Fallback image
                    if not photo_url or photo_url.startswith("data:"):
                        gallery_img = prod_soup.select_one("div.woocommerce-product-gallery__image img")
                        if gallery_img and safe_attribute_extract(gallery_img, "src").startswith("http"):
                            photo_url = safe_attribute_extract(gallery_img, "src")
                            print(f"🔁 Used fallback image for: {title}")
                        else:
                            print(f"⚠️ No usable image found for: {title}")

                    rate_limit(delay)
                except Exception as e:
                    print(f"❌ Failed to fetch product detail: {e}")

            # --- Download image ---
            if save_images and photo_url and photo_url.startswith("http"):
                safe_name = slugify(title)[:100]
                image_filename = os.path.join(IMAGE_FOLDER, f"{safe_name}.jpg")
                if not download_image(photo_url, image_filename):
                    image_filename = ""
            elif photo_url.startswith("data:"):
                print(f"⚠️ Skipped embedded image for: {title}")
                image_filename = "embedded SVG (not saved)"

            # --- Add to list ---
            products_data.append({
                "Product Name": title,
                "Price (With Reduction)": price_new,
                "Original Price": price_old,
                "Categories": categories,
                "Photo File": image_filename,
                "Photo URL": photo_url,
                "Description": description,
                "Product Page": product_link
            })

        page += 1

    return products_data



def scrape_all_categories(categories=None, save_images=True, delay=1, output_format="xlsx"):
    if categories is None:
        categories = CATEGORIES
    for category in categories:
        products = scrape_category(category, save_images=save_images, delay=delay)
        export_category_data(products, category, output_format=output_format)

def main():
    # You can customize these parameters
    categories = CATEGORIES  # or a subset
    save_images = True
    delay = 1
    output_format = "xlsx"  # or "csv"
    scrape_all_categories(categories, save_images, delay, output_format)

if __name__ == "__main__":
    main()

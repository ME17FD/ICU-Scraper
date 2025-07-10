#!/usr/bin/env python3
"""
ICU-scraper main entry point.

This script demonstrates how to use the restructured ICU-scraper project
with its modular architecture.
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.avito_scraper import scrape_avito
from scrapers.general_scraper import GeneralScraper
from utils.export import export_data


def demo_avito_scraper():
    """Demonstrate Avito scraper usage."""
    print("🔍 Demo: Avito Scraper")
    print("=" * 50)
    
    # Example URL for apartments in Casablanca
    url = "https://www.avito.ma/fr/maroc/appartement_casablanca"
    
    # Scrape 2 pages with custom fields
    custom_fields = {"title", "price", "location", "link"}
    results, fields = scrape_avito(url, pages=2, delay=1, fields=custom_fields)
    
    # Export results
    export_data(results, list(fields), url, 2, "xlsx", site_name="avito_ma")
    
    print(f"✅ Scraped {len(results)} items from Avito")
    print()


def demo_general_scraper():
    """Demonstrate General scraper usage."""
    print("🔍 Demo: General Scraper")
    print("=" * 50)
    
    # Example configuration for a generic e-commerce site
    config = {
        "site_name": "example_site",
        "base_url": "https://example.com",
        "headers": {"User-Agent": "Mozilla/5.0"},
        "container_selector": "div.product-item",
        "pagination": {
            "type": "parameter",
            "parameter": "page"
        },
        "fields": {
            "title": {
                "selector": "h2.product-title",
                "default": "N/A"
            },
            "price": {
                "selector": "span.price",
                "default": "N/A"
            },
            "link": {
                "selector": "a.product-link",
                "type": "attribute",
                "attribute": "href",
                "default": "N/A"
            }
        }
    }
    
    # Create scraper instance
    scraper = GeneralScraper(config)
    
    # Note: This is just a demonstration - the URL doesn't exist
    # In real usage, you would provide a valid URL
    print("ℹ️  General scraper configured (example only)")
    print("   To use with a real site, provide valid URL and configuration")
    print()


def main():
    """Main entry point."""
    print("🚀 ICU-scraper Demo")
    print("=" * 60)
    print()
    
    # Demo Avito scraper
    demo_avito_scraper()
    
    # Demo General scraper
    demo_general_scraper()
    
    print("📚 Usage Examples:")
    print("- Avito scraper: python -m scrapers.avito_scraper")
    print("- 1moment scraper: python -m scrapers.1moment_scraper")
    print("- General scraper: Use GeneralScraper class with custom config")
    print()
    print("📖 See README.md for detailed documentation")


if __name__ == "__main__":
    main() 
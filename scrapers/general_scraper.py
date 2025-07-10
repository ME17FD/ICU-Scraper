import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin
from typing import Dict, List, Optional, Union, Any
import re
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.export import export_general_data
from utils.helpers import fetch_soup, safe_text_extract, safe_attribute_extract, make_absolute_url, rate_limit


class GeneralScraper:
    """
    A flexible, configuration-driven web scraper that can adapt to different websites
    using JSON configuration files or dictionaries.
    """
    
    def __init__(self, config: Union[str, Dict], base_url: str = None):
        """
        Initialize the scraper with configuration.
        
        Args:
            config: Either a path to JSON config file or a config dictionary
            base_url: Base URL for the website (optional if in config)
        """
        self.config = self._load_config(config)
        self.base_url = base_url or self.config.get('base_url', '')
        self.session = requests.Session()
        self.session.headers.update(self.config.get('headers', {'User-Agent': 'Mozilla/5.0'}))
        
    def _load_config(self, config: Union[str, Dict]) -> Dict:
        """Load configuration from file or dictionary."""
        if isinstance(config, str):
            with open(config, 'r', encoding='utf-8') as f:
                return json.load(f)
        return config
    
    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a single page."""
        return fetch_soup(url, headers=self.session.headers, timeout=self.config.get('timeout', 10))
    
    def _extract_text(self, element, extractor: Dict) -> str:
        """Extract text from element based on extractor configuration."""
        if not element:
            return extractor.get('default', 'N/A')
        
        # Get text content
        text = safe_text_extract(element) if extractor.get('text', True) else str(element)
        
        # Apply transformations
        if 'regex' in extractor:
            match = re.search(extractor['regex'], text)
            text = match.group(1) if match else text
        
        if 'replace' in extractor:
            for old, new in extractor['replace'].items():
                text = text.replace(old, new)
        
        if 'strip_chars' in extractor:
            text = text.strip(extractor['strip_chars'])
        
        return text or extractor.get('default', 'N/A')
    
    def _extract_attribute(self, element, extractor: Dict) -> str:
        """Extract attribute from element."""
        if not element:
            return extractor.get('default', 'N/A')
        
        attr = extractor.get('attribute', 'href')
        value = safe_attribute_extract(element, attr)
        
        # Make absolute URL if needed
        if attr in ['href', 'src'] and value and not value.startswith('http'):
            value = make_absolute_url(value, self.base_url)
        
        return value or extractor.get('default', 'N/A')
    
    def _extract_field(self, container, field_config: Dict) -> Any:
        """Extract a single field from container element."""
        selector = field_config.get('selector')
        if not selector:
            return field_config.get('default', 'N/A')
        
        # Find element(s)
        if field_config.get('multiple', False):
            elements = container.select(selector)
        else:
            elements = [container.select_one(selector)]
        
        # Extract data
        if field_config.get('type') == 'attribute':
            if field_config.get('multiple', False):
                return [self._extract_attribute(el, field_config) for el in elements if el]
            else:
                return self._extract_attribute(elements[0], field_config)
        else:
            if field_config.get('multiple', False):
                return [self._extract_text(el, field_config) for el in elements if el]
            else:
                return self._extract_text(elements[0], field_config)
    
    def _parse_item(self, container) -> Dict:
        """Parse a single item from its container element."""
        item_data = {}
        
        for field_name, field_config in self.config['fields'].items():
            try:
                item_data[field_name] = self._extract_field(container, field_config)
            except Exception as e:
                print(f"⚠️ Error extracting {field_name}: {e}")
                item_data[field_name] = field_config.get('default', 'N/A')
        
        return item_data
    
    def _get_next_page_url(self, soup: BeautifulSoup, current_page: int) -> Optional[str]:
        """Get next page URL based on configuration."""
        pagination_config = self.config.get('pagination', {})
        
        if pagination_config.get('type') == 'parameter':
            # URL parameter based pagination
            param = pagination_config.get('parameter', 'page')
            base_url = pagination_config.get('base_url', self.base_url)
            return f"{base_url}?{param}={current_page + 1}"
        
        elif pagination_config.get('type') == 'next_link':
            # Next link based pagination
            next_selector = pagination_config.get('next_selector')
            if next_selector:
                next_link = soup.select_one(next_selector)
                if next_link:
                    href = next_link.get('href')
                    return urljoin(self.base_url, href) if href else None
        
        return None
    
    def scrape(self, url: str, max_pages: int = 1, delay: float = 1.0) -> List[Dict]:
        """
        Scrape data from the website.
        
        Args:
            url: Starting URL
            max_pages: Maximum number of pages to scrape
            delay: Delay between requests in seconds
            
        Returns:
            List of scraped items
        """
        results = []
        current_url = url
        
        for page in range(1, max_pages + 1):
            print(f"🔎 Scraping page {page}: {current_url}")
            
            soup = self._fetch_page(current_url)
            if not soup:
                break
            
            # Find item containers
            container_selector = self.config.get('container_selector')
            if not container_selector:
                print("❌ No container selector configured")
                break
            
            containers = soup.select(container_selector)
            print(f"📦 Found {len(containers)} items on page {page}")
            
            # Parse each item
            for container in containers:
                item_data = self._parse_item(container)
                if item_data:
                    results.append(item_data)
            
            # Get next page URL
            if page < max_pages:
                next_url = self._get_next_page_url(soup, page)
                if next_url and next_url != current_url:
                    current_url = next_url
                    rate_limit(delay)
                else:
                    print("📄 No more pages found")
                    break
        
        return results
    
    def export_data(self, data: List[Dict], filename: str = None, format: str = 'xlsx'):
        """Export scraped data to file."""
        site_name = self.config.get('site_name', 'scraped_data')
        return export_general_data(data, filename, format, site_name)


# Configuration examples and helper functions
def create_avito_config() -> Dict:
    """Create configuration for Avito.ma scraper."""
    return {
        "site_name": "avito_ma",
        "base_url": "https://www.avito.ma",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
        "container_selector": "a.sc-1jge648-0",
        "pagination": {
            "type": "parameter",
            "parameter": "o",
            "base_url": "https://www.avito.ma/fr/maroc/appartement_casablanca"
        },
        "fields": {
            "title": {
                "selector": "p[title]",
                "type": "attribute",
                "attribute": "title"
            },
            "price": {
                "selector": "p.sc-b57yxx-3",
                "replace": {"\u202f": ""}
            },
            "location": {
                "selector": "div.sc-b57yxx-11 p"
            },
            "details": {
                "selector": "div.sc-b57yxx-2 span span",
                "multiple": True,
                "type": "text"
            },
            "link": {
                "selector": "",
                "type": "attribute",
                "attribute": "href"
            },
            "image": {
                "selector": "div.sc-bsm2tm-2 img",
                "type": "attribute",
                "attribute": "src"
            },
            "date": {
                "selector": "div.sc-1wnmz4-2 p"
            },
            "seller": {
                "selector": "p.sc-1wnmz4-5"
            }
        }
    }


def create_generic_ecommerce_config() -> Dict:
    """Create a generic e-commerce configuration template."""
    return {
        "site_name": "generic_ecommerce",
        "base_url": "https://example.com",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
        "container_selector": ".product-item",
        "pagination": {
            "type": "next_link",
            "next_selector": "a.next-page"
        },
        "fields": {
            "title": {
                "selector": ".product-title",
                "default": "No Title"
            },
            "price": {
                "selector": ".price",
                "regex": r"[\d,.]+"
            },
            "image": {
                "selector": "img",
                "type": "attribute",
                "attribute": "src"
            },
            "link": {
                "selector": "a",
                "type": "attribute",
                "attribute": "href"
            },
            "rating": {
                "selector": ".rating",
                "regex": r"(\d+\.?\d*)"
            }
        }
    }


# Usage example
if __name__ == "__main__":
    # Example 1: Using Avito configuration
    config = create_avito_config()
    scraper = GeneralScraper(config)
    
    url = "https://www.avito.ma/fr/maroc/appartement_casablanca"
    results = scraper.scrape(url, max_pages=2, delay=1.0)
    
    scraper.export_data(results, format='xlsx')
    
    # Example 2: Using configuration from file
    # scraper = GeneralScraper('config.json')
    # results = scraper.scrape(url, max_pages=3)
    # scraper.export_data(results, 'my_data.csv', 'csv')
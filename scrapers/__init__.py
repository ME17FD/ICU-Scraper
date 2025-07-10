"""
ICU-scraper scrapers package.

This package contains specialized scrapers for different websites.
"""

from .avito_scraper import scrape_avito
from .general_scraper import GeneralScraper
# Note: 1moment_scraper module name starts with number, import with getattr
import importlib
moment_scraper = importlib.import_module('.1moment_scraper', __package__)
scrape_category = moment_scraper.scrape_category
scrape_all_categories = moment_scraper.scrape_all_categories

__all__ = [
    'scrape_avito',
    'GeneralScraper', 
    'scrape_category',
    'scrape_all_categories'
] 
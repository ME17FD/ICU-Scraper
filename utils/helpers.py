"""
Helper utilities for ICU-scraper.

This module provides common helper functions used across different scrapers.
"""

import requests
from bs4 import BeautifulSoup
import time
import re
import os
from typing import Optional, Dict, Any
from urllib.parse import urljoin


def fetch_soup(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 10) -> Optional[BeautifulSoup]:
    """
    Fetch and parse a webpage into BeautifulSoup object.
    
    Args:
        url: URL to fetch
        headers: Request headers (optional)
        timeout: Request timeout in seconds
        
    Returns:
        BeautifulSoup object or None if failed
    """
    if headers is None:
        headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return None


def safe_text_extract(element, default: str = "N/A") -> str:
    """
    Safely extract text from a BeautifulSoup element.
    
    Args:
        element: BeautifulSoup element
        default: Default value if extraction fails
        
    Returns:
        Extracted text or default value
    """
    if not element:
        return default
    
    try:
        text = element.get_text(strip=True)
        return text if text else default
    except Exception:
        return default


def safe_attribute_extract(element, attribute: str, default: str = "N/A") -> str:
    """
    Safely extract attribute from a BeautifulSoup element.
    
    Args:
        element: BeautifulSoup element
        attribute: Attribute name to extract
        default: Default value if extraction fails
        
    Returns:
        Attribute value or default value
    """
    if not element:
        return default
    
    try:
        value = element.get(attribute, "")
        return value if value else default
    except Exception:
        return default


def make_absolute_url(url: str, base_url: str) -> str:
    """
    Convert relative URL to absolute URL.
    
    Args:
        url: URL to convert
        base_url: Base URL for resolution
        
    Returns:
        Absolute URL
    """
    if not url:
        return ""
    
    if url.startswith(('http://', 'https://')):
        return url
    
    return urljoin(base_url, url)


def slugify(text: str) -> str:
    """
    Convert text to URL-friendly slug.
    
    Args:
        text: Text to convert
        
    Returns:
        URL-friendly slug
    """
    if not text:
        return ""
    
    # Remove special characters and replace with underscores
    slug = re.sub(r'[^\w\-_.]', '_', text)
    # Remove multiple consecutive underscores
    slug = re.sub(r'_+', '_', slug)
    # Remove leading/trailing underscores
    slug = slug.strip('_')
    
    return slug


def ensure_directory(directory: str) -> None:
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        directory: Directory path to ensure
    """
    os.makedirs(directory, exist_ok=True)


def download_image(url: str, filepath: str, timeout: int = 10) -> bool:
    """
    Download an image from URL to filepath.
    
    Args:
        url: Image URL
        filepath: Local filepath to save to
        timeout: Request timeout in seconds
        
    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.get(url, stream=True, timeout=timeout)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        
        return True
    except Exception as e:
        print(f"❌ Failed to download image {url}: {e}")
        return False


def rate_limit(delay: float = 1.0) -> None:
    """
    Implement rate limiting between requests.
    
    Args:
        delay: Delay in seconds
    """
    if delay > 0:
        time.sleep(delay)


def clean_price(price_text: str) -> str:
    """
    Clean price text by removing common formatting characters.
    
    Args:
        price_text: Raw price text
        
    Returns:
        Cleaned price text
    """
    if not price_text:
        return ""
    
    # Remove common formatting characters
    cleaned = price_text.replace('\u202f', '').replace('\xa0', ' ')
    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split())
    
    return cleaned


def validate_url(url: str) -> bool:
    """
    Basic URL validation.
    
    Args:
        url: URL to validate
        
    Returns:
        True if URL appears valid, False otherwise
    """
    if not url:
        return False
    
    # Basic URL pattern check
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url)) 
# ICU-scraper

A comprehensive, modular web scraping framework for extracting data from various e-commerce and classified advertisement websites. ICU-scraper provides specialized scrapers for different platforms with unified data export capabilities and a clean, maintainable architecture.

## 🚀 Features

- **Modular Architecture**: Clean separation of scrapers and utilities
- **Multi-platform Support**: Specialized scrapers for different websites
- **Flexible Field Selection**: Choose which data fields to extract
- **Multiple Export Formats**: CSV and Excel output with comprehensive metadata
- **Rate Limiting**: Built-in delays to respect website policies
- **Robust Error Handling**: Graceful handling of network and parsing errors
- **Data Validation**: Clean and structured data output
- **Extensible Design**: Easy to add new scrapers following established patterns

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies
```bash
# Clone the repository
git clone <repository-url>
cd ICU-scraper

# Install required packages
pip install -r requirements.txt
```

### Dependencies
- `requests>=2.31.0` - HTTP requests
- `beautifulsoup4>=4.12.0` - HTML parsing
- `pandas>=2.0.0` - Data manipulation
- `openpyxl>=3.1.0` - Excel file handling
- `lxml>=4.9.0` - Enhanced XML/HTML parsing

## 🏗️ Project Structure

```
ICU-scraper/
├── scrapers/                    # Specialized scrapers
│   ├── __init__.py             # Package initialization
│   ├── avito_scraper.py        # Avito.ma specialized scraper
│   ├── general_scraper.py      # General-purpose scraper
│   └── 1moment_scraper.py      # 1moment.ma e-commerce scraper
├── utils/                       # Shared utilities
│   ├── __init__.py             # Package initialization
│   ├── export.py               # Data export utilities
│   └── helpers.py              # Common helper functions
├── main.py                     # Main entry point with demos
├── README.md                   # This documentation
├── requirements.txt            # Python dependencies
└── .gitignore                 # Git ignore rules
```

## 🎯 Available Scrapers

### 1. Avito Scraper (`scrapers/avito_scraper.py`)

Specialized scraper for Avito.ma, Morocco's leading classified ads platform.

#### Features
- ✅ Extracts comprehensive listing data
- ✅ Supports pagination
- ✅ Configurable field selection
- ✅ Automatic data export with metadata
- ✅ Rate limiting and error handling

#### Available Fields
| Field | Description | Example |
|-------|-------------|---------|
| `title` | Listing title | "Appartement 3 pièces" |
| `price` | Item price | "850,000 DH" |
| `location` | Geographic location | "Casablanca" |
| `details` | Additional item details | "3 chambres, 2 salles de bain" |
| `link` | Direct link to listing | "https://www.avito.ma/..." |
| `seller` | Seller information | "Agence X" |
| `date` | Posting date | "Il y a 2 jours" |
| `image` | Main image URL | "https://img.avito.ma/..." |

#### Usage Examples

```python
from scrapers.avito_scraper import scrape_avito
from utils.export import export_data

# Basic usage - scrape apartments in Casablanca
url = "https://www.avito.ma/fr/maroc/appartement_casablanca"
results, fields = scrape_avito(url, pages=3)

# Export to Excel (default)
export_data(results, list(fields), url, 3, "xlsx", site_name="avito_ma")

# Custom field selection
custom_fields = {"title", "price", "location", "link"}
results, fields = scrape_avito(url, pages=2, fields=custom_fields)

# Export to CSV
export_data(results, list(fields), url, 2, "csv", site_name="avito_ma")
```

#### Configuration Options

```python
# Full configuration example
results, fields = scrape_avito(
    url="https://www.avito.ma/fr/maroc/voiture",
    pages=5,                    # Number of pages to scrape
    delay=2,                    # Delay between requests (seconds)
    fields={"title", "price", "location", "link"}  # Custom fields
)
```

### 2. General Scraper (`scrapers/general_scraper.py`)

A flexible, configuration-driven scraper that can adapt to different websites using JSON configuration files or dictionaries.

#### Features
- ✅ Configuration-driven scraping
- ✅ Support for various pagination methods
- ✅ Flexible field extraction with transformations
- ✅ Multiple data types (text, attributes, lists)
- ✅ Built-in error handling and validation

#### Configuration Example

```python
from scrapers.general_scraper import GeneralScraper

# Configuration for a generic e-commerce site
config = {
    "site_name": "example_site",
    "base_url": "https://example.com",
    "headers": {"User-Agent": "Mozilla/5.0"},
    "timeout": 10,
    "container_selector": "div.product-item",
    "pagination": {
        "type": "parameter",  # or "next_link"
        "parameter": "page"
    },
    "fields": {
        "title": {
            "selector": "h2.product-title",
            "default": "N/A"
        },
        "price": {
            "selector": "span.price",
            "replace": {"$": "", ",": ""},
            "default": "N/A"
        },
        "link": {
            "selector": "a.product-link",
            "type": "attribute",
            "attribute": "href",
            "default": "N/A"
        },
        "images": {
            "selector": "img.product-image",
            "type": "attribute",
            "attribute": "src",
            "multiple": True,
            "default": []
        }
    }
}

# Create scraper and use it
scraper = GeneralScraper(config)
results = scraper.scrape("https://example.com/products", max_pages=3, delay=1)
scraper.export_data(results, format="xlsx")
```

### 3. 1moment Scraper (`scrapers/1moment_scraper.py`)

Specialized scraper for [1moment.ma](https://1moment.ma), a Moroccan e-commerce platform.

#### Features
- ✅ Category-based scraping
- ✅ Product image downloading
- ✅ Price comparison (original vs. discounted)
- ✅ Product descriptions and details
- ✅ Automatic category discovery

#### Available Categories
- `make-up` - Cosmetics and beauty products
- `maman-bebe` - Baby and mother products
- `parfum` - Perfumes and fragrances
- `idees-cadeaux` - Gift ideas
- `complement-alimentaire-et-force` - Supplements
- `accessoires` - Accessories
- `parapharmacie` - Pharmacy products

#### Usage Examples

```python
from scrapers.1moment_scraper import scrape_category, scrape_all_categories

# Scrape a specific category
products = scrape_category("make-up", save_images=True, delay=1)

# Scrape all categories
scrape_all_categories(save_images=True, delay=1, output_format="xlsx")

# Scrape specific categories only
categories = ["make-up", "parfum"]
scrape_all_categories(categories, save_images=False, delay=2)
```

## 🛠️ Utilities

### Export Utilities (`utils/export.py`)

Centralized data export functionality supporting multiple formats with metadata.

#### Functions
- `export_data()` - Standard export with metadata
- `export_general_data()` - Export for general scraper
- `export_category_data()` - Category-specific export

#### Export Formats

**Excel Output**:
- `Listings` sheet: Main data with all extracted fields
- `Documentation` sheet: Scraping metadata and summary

**CSV Output**:
- Commented header with scraping metadata
- UTF-8 encoding for international characters

### Helper Utilities (`utils/helpers.py`)

Common helper functions used across all scrapers.

#### Key Functions
- `fetch_soup()` - Safe webpage fetching and parsing
- `safe_text_extract()` - Safe text extraction from elements
- `safe_attribute_extract()` - Safe attribute extraction
- `make_absolute_url()` - Convert relative URLs to absolute
- `slugify()` - Create URL-friendly slugs
- `download_image()` - Download images with error handling
- `rate_limit()` - Implement rate limiting
- `clean_price()` - Clean price formatting
- `validate_url()` - Basic URL validation

## 🚀 Quick Start

### 1. Basic Usage

```python
# Run the demo
python main.py

# Use Avito scraper directly
python -m scrapers.avito_scraper

# Use 1moment scraper
python -m scrapers.1moment_scraper
```

### 2. Programmatic Usage

```python
from scrapers.avito_scraper import scrape_avito
from utils.export import export_data

# Scrape apartments
url = "https://www.avito.ma/fr/maroc/appartement_casablanca"
results, fields = scrape_avito(url, pages=2)

# Export results
export_data(results, list(fields), url, 2, "xlsx")
```

### 3. Custom Scraper

```python
from scrapers.general_scraper import GeneralScraper

# Define your configuration
config = {
    "site_name": "my_site",
    "base_url": "https://example.com",
    "container_selector": "div.item",
    "fields": {
        "title": {"selector": "h1.title"},
        "price": {"selector": "span.price"}
    }
}

# Create and use scraper
scraper = GeneralScraper(config)
results = scraper.scrape("https://example.com/items", max_pages=3)
scraper.export_data(results)
```

## 📊 Output Examples

### Excel Output Structure

| title | price | location | details | link | seller | date | image |
|-------|-------|----------|---------|------|--------|------|-------|
| Appartement 3 pièces | 850,000 DH | Casablanca | 3 chambres, 2 salles de bain | https://... | Agence X | Il y a 2 jours | https://... |
| Villa 4 pièces | 1,200,000 DH | Rabat | 4 chambres, jardin | https://... | Particulier | Il y a 1 jour | https://... |

### Metadata Sheet
- **Site**: avito_ma
- **URL**: https://www.avito.ma/fr/maroc/appartement_casablanca
- **Pages Scraped**: 3
- **Fields**: title, price, location, details, link, seller, date, image
- **Total Items**: 74
- **Scraped**: 2025-07-10 23:08:45

## 🔧 Configuration

### Rate Limiting
```python
# Respectful scraping delays
delay = 2  # seconds between requests
```

### Headers
```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
```

### Error Handling
- **Network errors**: Automatic retry with proper error logging
- **Parsing errors**: Graceful handling of missing or malformed data
- **Rate limiting**: Built-in delays between requests

## 🚦 Best Practices

1. **Respect robots.txt**: Always check the website's robots.txt file
2. **Rate limiting**: Use appropriate delays between requests (1-3 seconds)
3. **Data validation**: Verify scraped data before processing
4. **Error handling**: Implement proper exception handling
5. **Monitoring**: Log scraping activities for debugging
6. **Legal compliance**: Always respect website terms of service

## 🔮 Future Enhancements

### Planned Scrapers
...

### Planned Features
- [ ] **Database Integration**: Direct export to PostgreSQL/MySQL
- [ ] **Real-time Monitoring**: Live data tracking and alerts
- [ ] **Advanced Filtering**: Complex search criteria and filters
- [ ] **Parallel Processing**: Multi-threaded scraping for better performance
- [ ] **Data Enrichment**: Integration with external data sources
- [ ] **Web Interface**: Simple web UI for configuration and monitoring
- [ ] **API Endpoints**: REST API for programmatic access
- [ ] **Scheduled Scraping**: Automated scraping with cron jobs

## ⚠️ Legal Considerations

- **Terms of Service**: Always review and comply with website terms
- **Rate Limiting**: Respect website server capacity and policies
- **Data Usage**: Use scraped data responsibly and legally
- **Privacy**: Respect user privacy and data protection laws
- **Educational Use**: This tool is designed for educational and research purposes

## 🐛 Troubleshooting

### Common Issues

1. **Connection timeouts**
   - **Solution**: Increase delay between requests
   - **Example**: `delay=3` instead of `delay=1`

2. **Parsing errors**
   - **Cause**: Website structure may have changed
   - **Solution**: Update selectors in scraper configuration

3. **Missing data**
   - **Cause**: Field selectors may be incorrect
   - **Solution**: Verify selectors using browser developer tools

4. **Export errors**
   - **Cause**: Insufficient write permissions
   - **Solution**: Check file permissions and disk space

### Debug Mode

Enable verbose logging for debugging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use the built-in print statements
# They provide detailed information about the scraping process
```

### Performance Optimization

```python
# For faster scraping (use responsibly)
delay = 0.5  # Minimum recommended delay

# For large datasets
pages = 10   # Limit pages to avoid overwhelming servers
```

## 📝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-scraper`
3. **Add your scraper** following the existing pattern:
   - Place in `scrapers/` directory
   - Use utility functions from `utils/`
   - Include proper error handling
   - Add comprehensive documentation
4. **Test your changes**: Ensure all scrapers still work
5. **Submit a pull request**

### Adding a New Scraper

1. Create `scrapers/your_site_scraper.py`
2. Import utilities: `from utils.helpers import *`
3. Import export: `from utils.export import export_data`
4. Follow the pattern of existing scrapers
5. Add to `scrapers/__init__.py`
6. Update this README

## 📄 License

[Add your license information here]

## 🤝 Support

For issues, questions, and contributions:

- **Issues**: Create an issue in the repository
- **Documentation**: Check this README and inline code comments
- **Examples**: See `main.py` for usage examples
- **Troubleshooting**: Review the troubleshooting section above

## 📈 Project Status

- ✅ **Avito Scraper**: Fully functional
- ✅ **General Scraper**: Fully functional
- ✅ **1moment Scraper**: Fully functional
- ✅ **Export Utilities**: Complete
- ✅ **Helper Functions**: Complete
- 🔄 **Documentation**: Updated and comprehensive
- 🚧 **Future Scrapers**: In development

---

**Note**: This scraper is designed for educational and research purposes. Always ensure compliance with website terms of service and applicable laws when scraping web data. Use responsibly and respect website policies.
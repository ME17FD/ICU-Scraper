# ICU-scraper

A comprehensive web scraping module for extracting data from various e-commerce and classified advertisement websites. ICU-scraper provides specialized scrapers for different platforms with unified data export capabilities.

## 🚀 Features

- **Multi-platform support**: Specialized scrapers for different websites
- **Flexible field selection**: Choose which data fields to extract
- **Multiple export formats**: CSV and Excel output with metadata
- **Rate limiting**: Built-in delays to respect website policies
- **Error handling**: Robust error handling and logging
- **Data validation**: Clean and structured data output

## 📦 Installation

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

## 🏗️ Module Structure

```
ICU-scraper/
├── scrapers/
│   ├── avito_scraper.py       # Avito.ma scraper
│   ├── [future_scraper].py    # Additional site scrapers
│   └── general_scraper.py     # General-purpose scraper
├── utils/
│   ├── export.py              # Data export utilities
│   └── helpers.py             # Common helper functions
├── README.md
└── requirements.txt
```

## 🎯 Scrapers

### Avito Scraper (`avito_scraper.py`)

Specialized scraper for Avito.ma, Morocco's leading classified ads platform.

#### Features
- Extracts comprehensive listing data
- Supports pagination
- Configurable field selection
- Automatic data export with metadata

#### Available Fields
- `title` - Listing title
- `price` - Item price
- `location` - Geographic location
- `details` - Additional item details
- `link` - Direct link to listing
- `seller` - Seller information
- `date` - Posting date
- `image` - Main image URL

#### Usage

```python
from avito_scraper import scrape_avito, export_data

# Basic usage - scrape apartments in Casablanca
url = "https://www.avito.ma/fr/maroc/appartement_casablanca"
results, fields = scrape_avito(url, pages=3)

# Export to Excel (default)
export_data(results, fields, url, pages=3, output_format="xlsx")

# Custom field selection
custom_fields = {"title", "price", "location", "link"}
results, fields = scrape_avito(url, pages=2, fields=custom_fields)

# Export to CSV
export_data(results, fields, url, pages=2, output_format="csv")
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

#### Output Format

**Excel Output**: Two sheets
- `Listings`: Main data with all extracted fields
- `Documentation`: Scraping metadata and summary

**CSV Output**: Single file with commented metadata header

#### Sample Output Structure

| title | price | location | details | link | seller | date | image |
|-------|-------|----------|---------|------|--------|------|-------|
| Appartement 3 pièces | 850,000 DH | Casablanca | 3 chambres, 2 salles de bain | https://... | Agence X | Il y a 2 jours | https://... |

## 🔧 Configuration

### Headers and Rate Limiting

The scraper uses appropriate headers and implements rate limiting to respect website policies:

```python
HEADERS = {"User-Agent": "Mozilla/5.0"}
BASE_URL = "https://www.avito.ma"
```

### Error Handling

- **Network errors**: Automatic retry with proper error logging
- **Parsing errors**: Graceful handling of missing or malformed data
- **Rate limiting**: Built-in delays between requests

## 📊 Export Features

### Excel Export
- Multi-sheet workbook with data and metadata
- Automatic filename generation with timestamp
- Comprehensive documentation sheet

### CSV Export
- Commented header with scraping metadata
- UTF-8 encoding for international characters
- Clean, structured data format

## 🚦 Best Practices

1. **Respect robots.txt**: Always check the website's robots.txt file
2. **Rate limiting**: Use appropriate delays between requests
3. **Data validation**: Verify scraped data before processing
4. **Error handling**: Implement proper exception handling
5. **Monitoring**: Log scraping activities for debugging

## 🔮 Future Enhancements

### Planned Scrapers
- **General scraper**: Universal scraper for various e-commerce sites
- **Multi-platform scraper**: Unified interface for multiple platforms
- **API integration**: Direct API access where available

### Planned Features
- **Database integration**: Direct export to databases
- **Real-time monitoring**: Live data tracking
- **Advanced filtering**: Complex search criteria
- **Parallel processing**: Multi-threaded scraping
- **Data enrichment**: Additional data sources integration

## ⚠️ Legal Considerations

- **Terms of Service**: Always review and comply with website terms
- **Rate limiting**: Respect website server capacity
- **Data usage**: Use scraped data responsibly and legally
- **Privacy**: Respect user privacy and data protection laws

## 🐛 Troubleshooting

### Common Issues

1. **Connection timeouts**: Increase delay between requests
2. **Parsing errors**: Check if website structure has changed
3. **Missing data**: Verify field selectors are correct
4. **Export errors**: Ensure proper write permissions

### Debug Mode

Enable verbose logging by modifying the print statements or implementing a logging system:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your scraper following the existing pattern
4. Include proper error handling and documentation
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🤝 Support

For issues and questions:
- Create an issue in the repository
- Check existing documentation
- Review troubleshooting section

---

**Note**: This scraper is designed for educational and research purposes. Always ensure compliance with website terms of service and applicable laws when scraping web data.
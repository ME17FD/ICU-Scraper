"""
Export utilities for ICU-scraper.

This module provides centralized data export functionality for all scrapers,
supporting multiple output formats with metadata.
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional


def export_data(
    data: List[Dict[str, Any]], 
    fields: List[str], 
    url: str, 
    pages_scraped: int, 
    output_format: str = "xlsx",
    filename: Optional[str] = None,
    site_name: Optional[str] = None
) -> str:
    """
    Export scraped data to file with metadata.
    
    Args:
        data: List of scraped items
        fields: List of field names
        url: Source URL that was scraped
        pages_scraped: Number of pages scraped
        output_format: Output format ("xlsx" or "csv")
        filename: Custom filename (optional)
        site_name: Name of the website (optional)
        
    Returns:
        Path to the exported file
    """
    if not data:
        print("⚠️ No data to export")
        return ""
    
    # Generate filename if not provided
    if not filename:
        now = datetime.now().strftime("%Y-%m-%d_%H-%M")
        base_name = url.split("/")[-1].split("?")[0] or (site_name or "scraped_results")
        filename = f"{base_name}_{now}.{output_format}"
    
    # Create documentation string
    doc_string = (
        f"ICU Scraper Summary\n"
        f"- URL: {url}\n"
        f"- Pages Scraped: {pages_scraped}\n"
        f"- Fields: {', '.join(fields)}\n"
        f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"- Total items: {len(data)}"
    )
    
    df = pd.DataFrame(data)
    
    if output_format.lower() == "csv":
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
    return filename


def export_general_data(
    data: List[Dict[str, Any]], 
    filename: Optional[str] = None, 
    format: str = 'xlsx',
    site_name: str = 'scraped_data'
) -> str:
    """
    Export data for general scraper with metadata.
    
    Args:
        data: List of scraped items
        filename: Custom filename (optional)
        format: Output format ("xlsx" or "csv")
        site_name: Name of the website
        
    Returns:
        Path to the exported file
    """
    if not data:
        print("⚠️ No data to export")
        return ""
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{site_name}_{timestamp}.{format}"
    
    df = pd.DataFrame(data)
    
    if format.lower() == 'csv':
        df.to_csv(filename, index=False, encoding='utf-8')
    else:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
            
            # Add metadata sheet
            metadata = {
                'Site': site_name,
                'Scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Items': len(data),
                'Fields': list(data[0].keys()) if data else []
            }
            meta_df = pd.DataFrame(list(metadata.items()), columns=['Key', 'Value'])
            meta_df.to_excel(writer, sheet_name='Metadata', index=False)
    
    print(f"✅ Data exported to {filename}")
    return filename


def export_category_data(
    products_data: List[Dict[str, Any]], 
    category: str, 
    output_format: str = "xlsx"
) -> str:
    """
    Export category-specific data (for 1moment scraper).
    
    Args:
        products_data: List of product data
        category: Category name
        output_format: Output format ("xlsx" or "csv")
        
    Returns:
        Path to the exported file
    """
    output_file = f"{category}.{output_format}"
    df = pd.DataFrame(products_data)
    
    if output_format.lower() == "csv":
        df.to_csv(output_file, index=False)
    else:
        df.to_excel(output_file, index=False)
    
    print(f"✅ Finished category: {category} → Saved to '{output_file}'")
    return output_file 
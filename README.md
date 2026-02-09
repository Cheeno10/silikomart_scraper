# Data Scraping Test Output

A Python-based web scraping script that collects Silikomart product data from BakeDeco.com and exports the results into an Excel file for analysis and review.

---

## Project Overview

This project demonstrates structured web scraping using:
- requests
- BeautifulSoup
- pandas

The script navigates a BakeDeco brand listing page, visits each product page, extracts relevant product information, and saves everything into a clean Excel spreadsheet.

---

## Data Fields Collected

- Brand  
- Product Name  
- MFR ID  
- Price  
- Stock Status  
- Category (breadcrumb-based)  
- Image URL  
- Product Description  
- Product Page URL  
- Scraped Source  

---

## Requirements

Python version:
- Python 3.8+

Required libraries:
```bash
pip install requests beautifulsoup4 lxml pandas openpyxl

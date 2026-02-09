import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

baseurl = 'https://www.bakedeco.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 OPR/126.0.0.0'
}

# Fetch the product listing page
r = requests.get(
    'https://www.bakedeco.com/nav/brand.asp?pagestart=1&categoryID=0&price=0&manufacid=551&sortby=&clearance=0&va=1',
    headers=headers
)
soup = BeautifulSoup(r.content, 'lxml')

# Collect product links
productlinks = set()
for item in soup.find_all("div", class_="prd_list_mid"):
    for link in item.find_all("a", href=True):
        href = link["href"]
        if "detail.asp" in href:
            full_link = urljoin(baseurl, href)
            productlinks.add(full_link)

print(f"Found {len(productlinks)} products\n")

# List to store all product data
all_products = []

# Loop through each product page
for currentLink in productlinks:
    print("Scraping:", currentLink)

    try:
        r = requests.get(currentLink, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'lxml')
    except requests.RequestException as e:
        print("Failed to fetch:", e)
        continue

    product_data = {} 
    product_data['URL'] = currentLink

        # ---------- MFR ID ----------
    MFRID_div = soup.find('div', class_='item-number')

    product_data['MFR ID'] = 'N/A' 

    if MFRID_div:
        arr = MFRID_div.get_text(strip=True).split()
        if len(arr) >= 4:
            mfr = arr[3][:-4]
            if mfr:
                product_data['MFR ID'] = mfr

    # ---------- TITLE / BRAND ----------
    title_div = soup.find('div', class_='prod-title')
    if title_div:
        full_title = title_div.get_text(strip=True)
        brand = full_title.split()[0] if full_title else ''
        prodName = full_title.split('Item')[0].strip() if full_title else ''
        prodName = " ".join(prodName.split()[1:]) if prodName else ''
        product_data['Brand'] = brand
        product_data['Product Name'] = prodName
    else:
        product_data['Brand'] = ''
        product_data['Product Name'] = ''

    # ---------- IMAGE ----------
    img_div = soup.find('div', class_='prod-img')
    if img_div:
        img = img_div.find('img')
        product_data['Image URL'] = urljoin(baseurl, img['src']) if img and img.get('src') else ''
    else:
        product_data['Image URL'] = ''
    
    # ---------- PRICE ----------
    price_div = soup.find('div', class_='you-pay red-color')
    product_data['Price'] = ''  # Default

    if price_div:
        price_text = price_div.get_text(strip=True)
        
        if "Price:" in price_text:
            # Normal price
            product_data['Price'] = price_text.split("Price:")[-1].strip()
        elif "You Pay:" in price_text:
            # Sale price fallback
            sale_price = price_text.split("You Pay:")[-1].strip()
            product_data['Price'] = f"Sale: {sale_price}"


    # ---------- STOCK STATUS ----------
    stock_status = []
    for div in soup.select('div.green-checked-icon'):
        text = div.find(string=True, recursive=False)
        if text:
            stock_status.append(text.strip())

    product_data['Stock Status'] = " | ".join(stock_status) if stock_status else 'N/A'



   # ---------- CATEGORY / BREADCRUMB ----------
    category_div = soup.find('div', class_='bread')
    if category_div:
        all_texts = [s.strip() for s in category_div.stripped_strings if s.strip() != '>>']
        all_texts = all_texts[1:]
        product_data['Category'] = ' / '.join(all_texts) if all_texts else ''
    else:
        product_data['Category'] = ''

    # ---------- DESCRIPTION ----------
    desc_div = soup.find('div', class_='description-item')
    product_data['Description'] = desc_div.get_text(strip=True) if desc_div else ''

    # ---------- SCRAPED AT ----------
    product_data['Scraped At'] = baseurl

    # Add this product's data to the list
    all_products.append(product_data)

 # ---------- PRINT PRODUCT TO TERMINAL ----------
    print(f"Brand: {product_data['Brand']}")
    print(f"Product Name: {product_data['Product Name']}")
    print(f"MFR ID: {product_data['MFR ID']}")
    print(f"Price: {product_data['Price']}")
    print(f"Stock Status: {product_data['Stock Status']}")
    print(f"Category: {product_data['Category']}")
    print(f"Image URL: {product_data['Image URL']}")
    print(f"Description:\n{product_data['Description']}")
    print("============================\n")
    
# Create a DataFrame and export to Excel
df = pd.DataFrame(all_products)
df.to_excel('Dacoco_CheenoMari_SILIKOMART_20260210.xlsx', index=False)
print("All data exported to Dacoco_CheenoMari_SILIKOMART_20260210.xlsx")

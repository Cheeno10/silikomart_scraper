import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.bakedeco.com"
START_URL = "https://www.bakedeco.com/nav/brand.asp?pagestart=1&categoryID=0&price=0&manufacid=551&sortby=&clearance=0&va=1"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

r = requests.get(START_URL, headers=HEADERS)
soup = BeautifulSoup(r.content, "lxml")
product_links = set()

for prd_column in soup.find_all("div", class_="prd_list_mid"):
            for link in prd_column.find_all("a", href=True):
                href = link["href"]
                if "detail.asp" in href:
                    full_link = href
                    product_links.add(full_link)
                    print(full_link)

print(f"Found {len(product_links)} unique product links.")
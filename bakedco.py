import requests
from bs4 import BeautifulSoup

baseurl = 'https://www.bakedeco.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 OPR/126.0.0.0'
}


r = requests.get('https://www.bakedeco.com/nav/brand.asp?pagestart=1&categoryID=0&price=0&manufacid=551&sortby=&clearance=0&va=1', headers=headers)
soup = BeautifulSoup(r.content, 'lxml')

productlist = soup.find_all('div', class_='product')

productlinks = set()

for item in soup.find_all("div", class_="prd_list_mid"):
    for link in item.find_all("a", href=True):
        href = link["href"]
        if "detail.asp" in href:
            full_link = href
            productlinks.add(full_link)
            print(full_link)

print((len(productlinks)))

testlink = 'https://www.bakedeco.com/detail.asp?id=33381&categoryid=0'

r = requests.get(testlink, headers=headers)

soup = BeautifulSoup(r.content, 'lxml')

title_div = soup.find('div', class_='prod-title')

if title_div:
    Brand = title_div.get_text(strip=True).split()[0]
    print(Brand)
    
if title_div:
    prodName = title_div.get_text(strip=True)
    prodName = prodName.split('Item')[0].strip()
    prodName = " ".join(prodName.split()[1:])
    print(prodName)

MFRID_div = soup.find('div', class_='item-number')

if MFRID_div:
    arr = MFRID_div.get_text(strip=True).split()
    print(arr[3][:-4])

print (testlink)

img_div = soup.find('div', class_='prod-img')

if img_div:
    img = img_div.find('img')
    if img and img.get('src'):
        print(baseurl + img['src'])

stock_status = []

for div in soup.select('div.green-checked-icon'):
    text = div.find(string=True, recursive=False)
    if text:
        stock_status.append(text.strip())

if stock_status:
    print(" ".join(stock_status))


category_div = soup.find('div', class_='bread')
if category_div:
    all_texts = [s.strip() for s in category_div.stripped_strings if s.strip() != '>>']
    all_texts = all_texts[1:]
    formatted_category = ' / '.join(all_texts)
    print(formatted_category)


desc_div = soup.find('div', class_='description-item')
if desc_div:
    description = desc_div.get_text(strip=True)
    print(description)


print("Scraped at " + baseurl)
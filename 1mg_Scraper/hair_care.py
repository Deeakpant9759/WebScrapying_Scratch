from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

ua = UserAgent()
headers = {
    "User-Agent": ua.random,
    "Accept-Language": "en-US,en;q=0.9"
}

def get_page_html(url):
    res = requests.get(url=url, headers=headers)
    if res.status_code == 200:
        return res.content
    else:
        print(f"Failed to retrieve page, status code: {res.status_code}")
        return None
def Title_extract(soup):
    container = soup.find('div', class_="style__product-description___2XaG0")
    title_span = container.find('div', class_="style__pro-title___2QwJy")
    title = title_span.get_text(strip=True) if title_span else "No Title"
    return title

def Package_extract(soup):
    container = soup.find('div', class_="style__product-description___2XaG0")
    package_span = container.find('div', class_="style__pack-size___2JQG7")
    package = package_span.get_text(strip=True) if package_span else "No Package"
    return package

def MRP_extract(soup):
    container = soup.find('div', class_="style__product-pricing___38PRR")
    mrp_span = container.find('span', class_="style__discount-price___25Bya")
    mrp = mrp_span.get_text(strip=True) if mrp_span else "No MRP"
    return mrp
def URL_extract(soup):
    link_tag = soup.find('a', class_="style__product-link___UB_67")
    product_url = link_tag['href'] if link_tag else "No URL"
    base_url = "https://www.1mg.com"
    full_url = base_url + product_url if product_url != "No URL" else product_url
    return full_url

def Data_Extraction(soup):
    product_info = {}
    product_info['Name'] = Title_extract(soup)
    product_info['M.R.P'] = MRP_extract(soup)
    product_info['Package'] = Package_extract(soup)
    product_info['URL'] = URL_extract(soup)
    print(product_info)

def extract_hair_care_products(url):
    html = get_page_html(url)
    if html:
        big_soup = BeautifulSoup(html, "html.parser")
        Data = big_soup.find_all("div",class_ ="col-md-3 col-sm-4 col-xs-6 style__container___1TL2R ")
        for soup in Data:
            Data_Extraction(soup)
    else:
        print("No HTML to parse.")

# Run
if __name__ == "__main__":  
    for i in range(1,38):
        url = f"https://www.1mg.com/categories/hair-care/hair-oils-566?filter=true&page={i}"
        extract_hair_care_products(url)


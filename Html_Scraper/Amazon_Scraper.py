from datetime import datetime
import requests
import bs4
import csv
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
request_headers = {
    "User-Agent": useragent,
    "Accept-Language": "en-US,en;q=0.5"
}
no_threads = 10
def get_page_html(url):
    res = requests.get(url=url,headers=request_headers)
    return res.content

def get_product_price(soup):
    # Price (full, with ₹)
    container = soup.find('div',class_ = 'a-section a-spacing-none aok-align-center aok-relative')
    if container:
        target_span = container.find('span',class_='a-price-whole')
        if target_span:
            text_value = target_span.get_text(strip=True).replace(',','')
            return text_value
def get_title_of_product(soup):
    container = soup.find('div',id="titleSection")
    if container:
        target_span = container.find('span',id="productTitle")
        if target_span:
            text_value = target_span.text.strip().replace('\u200e', '')
            return text_value
def get_rating(soup):
    container = soup.find('div',id="averageCustomerReviews")
    if container:
        target_span = container.find('span',class_="a-icon-alt")
        if target_span:
            text_value = target_span.text.strip().replace('\u200e', '')
            return text_value
def get_Product_Tech(soup):
    details = {}
    container = soup.find('div',id="prodDetails")
    data_Tech = soup.findAll('table',class_="a-keyvalue prodDetTable")
    for data_Table in data_Tech:
        table_Rows = data_Table.findAll('tr')
        for row in table_Rows:
            row_key = row.find('th').text.strip().replace('\u200e', '')
            row_value = row.find('td').text.strip().replace('\u200e', '')
            details[row_key] = row_value
    return details

def extract_product_info(url,output):
    product_info={}
    #print(url)
    html = get_page_html(url=url)
    soup = bs4.BeautifulSoup(html,'html.parser')
    product_info['Price'] = get_product_price(soup)
    product_info['Title'] = get_title_of_product(soup)
    product_info['rating']=get_rating(soup)
    product_info.update(get_Product_Tech(soup))
    output.append(product_info)
if __name__ == "__main__":
    products_data =[]
    urls = []
    with open(r"Html_Scraper\Amazon_products.csv", newline='') as csvfile:
         urls = list(csv.reader(csvfile, delimiter=","))
    with ThreadPoolExecutor(max_workers = no_threads) as excutor:
        for wkn in tqdm(range(0,len(urls))):
            excutor.submit(extract_product_info,urls[wkn][0],products_data)
        
    out_file_name = 'output-{}.csv'.format(datetime.today().strftime('%d-%m-%Y'))
    with open(out_file_name, 'w', newline='', encoding='utf-8') as outputfile:
        writer = csv.writer(outputfile)
        if products_data:
            # Write header
            writer.writerow(products_data[0].keys())
            # Write each product row
            for product in products_data:
                # Make sure order matches header keys
                row = [product.get(k, '') for k in products_data[0].keys()]
                writer.writerow(row)



            
           


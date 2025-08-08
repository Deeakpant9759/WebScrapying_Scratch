from datetime import datetime
import requests
import bs4
import csv

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
request_headers = {
    "User-Agent": useragent,
    "Accept-Language": "en-US,en;q=0.5"
}

def get_page_html(url):
    res = requests.get(url=url,headers=request_headers)
    return res.content

def get_product_price(soup):
    main_price_sapn = soup.find('span',class_ ="a-price-whole").get_text()
    return(main_price_sapn)

def extract_product_info(url):
    product_info={}
    print(f"Extract the data of {url}")
    html = get_page_html(url=url)
    soup = bs4.BeautifulSoup(html,'html.parser')
    product_info['Price'] = get_product_price(soup)
    return product_info



if __name__ == "__main__":
    with open(r"C:\Users\MICILMEDS\Battel_with_Codes\WebScrapying_Scratch\Html_Scraper\Amazon_products.csv",newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter=",")
        for rw in reader:
            url = rw[0]
            print(extract_product_info(url))
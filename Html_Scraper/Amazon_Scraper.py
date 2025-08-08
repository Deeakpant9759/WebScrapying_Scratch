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
def extract_product_info(url):
    print(f"Extract the data of {url}")
    html = get_page_html(url=url)
    return html

if __name__ == "__main__":
    with open(r"D:\Programing Playground\WebScrapying_Scratch\Html_Scraper\Amazon_products.csv",newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter=",")
        for rw in reader:
            url = rw[0]
            print(extract_product_info(url))
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
    response = requests.get(url=url,headers=request_headers)
    return response.content

def Extract_Prouct_info(url):
    print(f"Extracting the Product Info of {url}")
    data = get_page_html(url=url)
    return data


if __name__ == "__main__":
    #with open(r"D:\Programing Playground\WebScrapying_Scratch\1mg_Scraper\1mg_Data.csv",newline='') as csvfile:
        #reader = csv.reader(csvfile,delimiter=",")
        print(Extract_Prouct_info("https://www.1mg.com/drugs/peggrafeel-6mg-injection-172936"))

            
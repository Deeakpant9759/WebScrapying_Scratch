from bs4 import BeautifulSoup
import requests
import smtplib
import time
import datetime
# Connect to Website and pull in data

URL = 'https://www.1mg.com/drugs/duolin-3-respules-3ml-480395'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

page=requests.get(URL,headers=headers)

soup=BeautifulSoup(page.content,'html.parser')

outer_div = soup.find("div", class_="DrugHeader__prescription-req___34WVy")

# Extract text from the span inside it
text = outer_div.find("span").get_text(strip=True)


print(text)
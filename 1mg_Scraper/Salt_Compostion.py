from bs4 import BeautifulSoup
import requests
import smtplib
import time
import datetime
# Connect to Website and pull in data

URL = 'https://www.1mg.com/drugs/azithral-500-tablet-325616'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

page=requests.get(URL,headers=headers)

soup=BeautifulSoup(page.content,'html.parser')

div_tag = soup.find("div", class_="saltInfo DrugHeader__meta-value___vqYM0")
a_tag = div_tag.find("a")

# Extract text from the span inside it
text = a_tag.get_text(strip=True)


print(text)
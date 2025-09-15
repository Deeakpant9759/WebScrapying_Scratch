from bs4 import BeautifulSoup
import requests
import fake_useragent
import os
import pandas as pd
from pathlib import Path
data = []
df = pd.DataFrame(data)
x = int(input("Enter Number of Pages to Scrape: "))
Img_folder = input("Enter Folder Name: ")
excel_name = Img_folder
url_input = input("Enter URL: ")
x += 1
useragent = fake_useragent.UserAgent().random
headers = {'user-agent': useragent}
base_url = f"{url_input}page/{{}}/"
for i in range(1, x):
    url = base_url.format(i)
    HTML = requests.get(url, headers=headers).text
    soup = BeautifulSoup(HTML, 'html.parser')
    products = []

    # Loop through each product container
    for product in soup.find_all("div", class_="ltn__product-item"):
        # Extract product name
        name_tag = product.find("h2", class_="product-title")
        name = name_tag.get_text(strip=True) if name_tag else None

        # Extract image URL
        img_tag = product.find("img")
        img_url = img_tag["src"] if img_tag else None

        if name and img_url:
            products.append({"name": name, "image_url": img_url})

    # Create folder for downloads
    
    Path(f"downloaded_products\\{Img_folder}").mkdir(parents=True, exist_ok=True)

    # Download images
    for i, p in enumerate(products, start=1):
        name = p["name"].replace(" ", "_")  # replace spaces for safe filenames
        url = p["image_url"]

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            file_path = os.path.join(f"downloaded_products\\{Img_folder}", f"{name}.jpg")
            with open(file_path, "wb") as f:
                f.write(response.content)

            print(f"✅ {i}. Downloaded {name}.jpg")
            print(f"   From: {url}")

        except Exception as e:
            print(f"❌ {i}. Failed {url} ({e})")
    df = pd.concat([df, pd.DataFrame(products)], ignore_index=True)
    df.to_excel(f"{excel_name}.xlsx", index=False)  # Save data to Excel
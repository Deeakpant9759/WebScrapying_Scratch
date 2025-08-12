from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import os
from datetime import date
import json

CHROME_DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver.exe")
op = webdriver.ChromeOptions()
op.add_experimental_option("detach", True)
op.add_experimental_option("excludeSwitches", ["enable-logging"])
op.add_argument("--log-level=3")
service = Service(CHROME_DRIVER_PATH)

DRIVER = webdriver.Chrome(service=service, options=op)

def main():
    try:
        DRIVER.get("https://www.instagram.com/")
        input("Bot operation completed. Press any key to exit...")
        DRIVER.quit()
    except Exception as e:
        print(e)
        DRIVER.quit()
if __name__ == '__main__':
    main()

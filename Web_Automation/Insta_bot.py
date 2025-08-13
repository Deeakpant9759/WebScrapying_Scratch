from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time

def login(driver,nameuser='_deepak__pant_', passw='9759894066'):
    username = driver.find_element(By.CSS_SELECTOR,value ='input[aria-label="Phone number, username, or email"]')
    password = driver.find_element(By.CSS_SELECTOR,value ='input[aria-label="Password"]')
    username.clear()
    password.clear()
    username.send_keys(nameuser)
    password.send_keys(passw)
    login_button = driver.find_element(By.CSS_SELECTOR,value = 'button[type="submit"]')
    login_button.click()


def main():
    CHROME_DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver.exe")
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")
    
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get("https://www.instagram.com/")
        # Optional wait for page to load
        time.sleep(4)
        login(driver)
        input("Bot operation completed. Press any key to exit...")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()

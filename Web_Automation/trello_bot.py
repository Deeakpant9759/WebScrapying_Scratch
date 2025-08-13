from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time


def login(driver, email='deepakpant9759@gmail.com', Password='9759894066'):
    partial_url = 'https://id.atlassian.com/login?'
    login_button = driver.find_element(By.XPATH, f'//a[contains(@href, "{partial_url}")]')
    login_button.click()
    time.sleep(5)  # Wait for the login page to load
    ##Email Input
    email_input = driver.find_element(By.CSS_SELECTOR,value = 'input[name=username]')
    email_input.clear()
    email_input.send_keys(email)
    Click_button = driver.find_element(By.CSS_SELECTOR,value = 'button[id="login-submit"]')
    Click_button.click()
    time.sleep(4)  # Wait for the password input to load
    ##password input
    Password_input = driver.find_element(By.CSS_SELECTOR, value='input[name=password]')
    Password_input.clear()
    Password_input.send_keys(Password)
    Click_button = driver.find_element(By.CSS_SELECTOR,value = 'button[id="login-submit"]')
    Click_button.click()

def main():
    CHROME_DRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver.exe')
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://trello.com/")
        time.sleep(5)  # Wait for the page to load
        login(driver)
    except Exception as e:
        print(f"Error occurred: {e}")
        driver.quit()
        return


if __name__ == "__main__":
    main()
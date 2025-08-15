from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time
from datetime import date

def login(driver, email='deepakpant9759@gmail.com', Password='9759894066'):
    partial_url = 'https://id.atlassian.com/login?'
    login_button = driver.find_element(By.XPATH, f'//a[contains(@href, "{partial_url}")]')
    login_button.click()
    time.sleep(3)  # Wait for the login page to load
    ##Email Input
    email_input = driver.find_element(By.CSS_SELECTOR,value = 'input[name=username]')
    email_input.clear()
    email_input.send_keys(email)
    Click_button = driver.find_element(By.CSS_SELECTOR,value = 'button[id="login-submit"]')
    Click_button.click()
    time.sleep(2)  # Wait for the password input to load
    ##password input
    Password_input = driver.find_element(By.CSS_SELECTOR, value='input[name=password]')
    Password_input.clear()
    Password_input.send_keys(Password)
    Click_button = driver.find_element(By.CSS_SELECTOR,value = 'button[id="login-submit"]')
    Click_button.click()
    time.sleep(2)  
    nevigate_to(driver)

def screenshot(driver):
    time.sleep(2)
    date_str = date.today().strftime("%Y-%m-%d")
    fpath = os.path.join(os.getcwd(), 'Downloads', f'{date_str}.png')
    os.makedirs(os.path.dirname(fpath), exist_ok=True)
    driver.save_screenshot(fpath)


def nevigate_to(driver):
    time.sleep(4)
    driver.find_element(By.XPATH,"//a[@title='Bot Borad']").click()
    time.sleep(2)
def Task_todo(driver):
    time.sleep(3)
    driver.find_element(By.XPATH,"//button[@data-testid='list-add-card-button' and @aria-label='Add a card in To Do']").click()
    time.sleep(2)
    card_input = driver.find_element(By.XPATH, "//textarea[@data-testid='list-card-composer-textarea']")
    card_input.click()
    time.sleep(1)
    card_input.send_keys("First time successful")
    card_input.send_keys(Keys.RETURN)  # Submit the card
    time.sleep(2)

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
        time.sleep(3)  # Wait for the page to load
        login(driver)
        Task_todo(driver)
        screenshot(driver)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()
        return


if __name__ == "__main__":
    main()
    
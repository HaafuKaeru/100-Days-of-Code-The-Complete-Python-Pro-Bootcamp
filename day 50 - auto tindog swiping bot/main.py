import os
import dotenv
import time

from selenium import webdriver
from selenium.common import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


dotenv.load_dotenv("../.env")
MY_TINDOG_URL = os.getenv("tindog_url")
MY_EMAIL = os.getenv("my_email")
MY_PASS = os.getenv("hundred_days_python_password")

# crhome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, timeout=2)
driver.get(MY_TINDOG_URL)

# login
login_button = driver.find_element(By.CSS_SELECTOR, value=".btn-tindog-login.tindog-login-pill")
login_button.click()
facebark_button = driver.find_element(By.CSS_SELECTOR, value=".btn-facebark")
wait.until(ec.element_to_be_clickable(facebark_button))
facebark_button.click()

# switch to new window
base_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)

# login to facebark
email_input = driver.find_element(By.NAME, value="email")
email_input.send_keys(MY_EMAIL)
pass_input = driver.find_element(By.NAME, value="pass")
pass_input.send_keys(MY_PASS)
login_button = driver.find_element(By.CSS_SELECTOR, value="form button")
login_button.click()

# accept location and cookies (primary button) but not notifications (secondary button)
driver.switch_to.window(base_window)
button_orders = {
    0: "btn-primary",
    1: "btn-secondary",
    2: "btn-primary",
}
for i in range(3):
    selector = (By.CSS_SELECTOR, f"button.{button_orders[i]}")
    wait.until(ec.presence_of_element_located(selector))
    button = driver.find_element(*selector)
    button.click()

# main page
like_button_selector = (By.CSS_SELECTOR, ".btn-like")
wait.until(ec.presence_of_element_located(like_button_selector))
like_button = driver.find_element(*like_button_selector)
wait.until(ec.element_to_be_clickable(like_button))

while True:
    time.sleep(1)
    try:
        like_button = driver.find_element(*like_button_selector)
        like_button.click()
    except ElementClickInterceptedException:
        popup_link = driver.find_element(By.CSS_SELECTOR, value=".match-popup-link")
        popup_link.click()
    except NoSuchElementException:
        break

driver.quit()
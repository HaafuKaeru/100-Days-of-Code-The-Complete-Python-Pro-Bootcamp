import os
import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec


dotenv.load_dotenv("../.env")
GOOGLE_FORM_URL = os.getenv("google_form_url")

# chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")


class GoogleFormManager:

    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, timeout=2)
        self.url = GOOGLE_FORM_URL
        self.driver.get(self.url)

    def submit_form(self, data: tuple):
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type^='text']")
        self.wait.until(ec.element_to_be_clickable(inputs[0]))
        # order of info in google form and data must match
        for i in range(3):
            inputs[i].send_keys(data[i])
        submit_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Submit')]")
        submit_button.click()
        submit_again = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Submit another response')]")
        self.wait.until(ec.element_to_be_clickable(submit_again))
        submit_again.click()

    def close(self):
        self.driver.quit()
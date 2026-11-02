import os
import dotenv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys


dotenv.load_dotenv("../.env")

# chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")


MY_EMAIL = os.getenv("my_email")
MY_PASSWORD = os.getenv("share_a_naan_pass")
# SIMILAR_ACCOUNT = "chefsteps"
# SIMILAR_ACCOUNT = "rordongamsay"
SIMILAR_ACCOUNT = "elaineducasse"
BASE_URL = "https://app.100daysofpython.dev/services/share-a-naan"
LOGIN_URL = f"{BASE_URL}/login"


class InstaFollower:

    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, timeout=2)
        self.my_email = MY_EMAIL
        self.my_password = MY_PASSWORD
        self.base_url = BASE_URL
        self.login_url = LOGIN_URL
        self.similar_account = SIMILAR_ACCOUNT

    def login(self):
        self.driver.get(self.login_url)
        input_email = self.driver.find_element(By.ID, "username")
        input_email.send_keys(self.my_email)
        input_password = self.driver.find_element(By.ID, "password")
        input_password.send_keys(self.my_password)
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button")
        login_button.click()
        # dismiss login pop-up
        dismiss_login_details = self.driver.find_element(By.CLASS_NAME, "naan-popup-dismiss")
        dismiss_login_details.click()
        # dismiss notifications pop-up
        dismiss_notifications = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        dismiss_notifications.click()

    def find_followers(self) -> list[WebElement]:
        self.driver.get(self.base_url + "/u/" + self.similar_account)
        followers_button = self.driver.find_element(By.CSS_SELECTOR, ".naan-followers-link")
        followers_button.click()
        # scroll until the end of followers list
        followers_dvis_selector = (By.CSS_SELECTOR, ".naan-follower-row")
        followers_divs = self.driver.find_elements(*followers_dvis_selector)
        while True:
            n = len(followers_divs)
            self.driver.find_element(By.CSS_SELECTOR, ".followers-scroll").send_keys(Keys.END)
            time.sleep(1)
            followers_divs = self.driver.find_elements(*followers_dvis_selector)
            if len(followers_divs) == n:
                break
        return followers_divs

    def follow(self, div_element):
        name = div_element.find_element(By.CSS_SELECTOR, ".naan-sub").text
        button = div_element.find_element(By.CSS_SELECTOR, ".naan-follow-btn")
        if "is-following" not in button.get_attribute("class"):
            button.click()
            print(f"Followed: {name}")


bot = InstaFollower()
bot.login()
followers_list = bot.find_followers()
for follower in followers_list:
    bot.follow(follower)
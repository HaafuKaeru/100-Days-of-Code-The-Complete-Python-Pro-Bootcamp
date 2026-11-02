import os
import dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec


dotenv.load_dotenv("../.env")

# chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")


PROMISED_DOWN = 1000
PROMISED_UP = 1000
Y_URL = os.getenv("y_login_url")
Y_EMAIL = os.getenv("y_email")
Y_PASS = os.getenv("y_pass")
SPEEDTEST_URL = "https://www.speedtest.net/"


class InternetSpeedTwitterBot:

    def __init__(self):
        self.exp_down = PROMISED_DOWN
        self.exp_up = PROMISED_UP
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, timeout=2)  # general wait object
        self.y_url = Y_URL
        self.y_email = Y_EMAIL
        self.y_password = Y_PASS
        self.speedtest_url = SPEEDTEST_URL

    def get_internet_speed(self) -> dict:
        self.driver.get(self.speedtest_url)
        # reject privacy policy
        policy_reject_selector = (By.CSS_SELECTOR, "#onetrust-reject-all-handler")
        self.wait.until(ec.presence_of_element_located(policy_reject_selector))
        policy_reject_button = self.driver.find_element(*policy_reject_selector)
        policy_reject_button.click()
        # start speed test
        go_button_selector = (By.CSS_SELECTOR, "button h1")
        go_button = self.driver.find_element(*go_button_selector)
        self.wait.until(ec.element_to_be_clickable(go_button))
        go_button.click()
        test_wait = WebDriverWait(self.driver, timeout=60)  # speed test wait object
        # dismiss pop-up
        popup_selector = (By.CSS_SELECTOR, ".MuiDialogContent-root")
        test_wait.until(ec.presence_of_element_located(popup_selector))
        popup_content = self.driver.find_element(*popup_selector)
        a_elements = popup_content.find_elements(By.CSS_SELECTOR, "a")
        back_button = a_elements[-1]  # last link dismisses the pop-up
        back_button.click()
        # get results
        results = self.driver.find_elements(By.CSS_SELECTOR, "h3")
        down = results[0].text
        up = results[1].text
        provider = results[3].text
        results_dict = {
            "down": f"{down.split('.')[0]}",
            "up": f"{up.split('.')[0]}",
            "provider": provider,
        }
        # self.driver.quit()
        return results_dict

    def tweet_at_provider(self, text: str):
        self.driver.get(self.y_url)
        # login
        email_input = self.driver.find_element(By.CSS_SELECTOR, "input[id*='email']")
        email_input.send_keys(self.y_email)
        pass_input = self.driver.find_element(By.CSS_SELECTOR, "input[id*='password']")
        pass_input.send_keys(self.y_password)
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".y-btn-primary.y-login-submit")
        login_button.click()
        # make post
        tweet_input = self.driver.find_element(By.CSS_SELECTOR, "#tweet-compose")
        tweet_input.send_keys(text)
        post_button = self.driver.find_element(By.CSS_SELECTOR, "#post-btn")
        post_button.click()


bot = InternetSpeedTwitterBot()

measurement = bot.get_internet_speed()
print(measurement)

def make_complaint(direction: str, expected: int):
    complain_text = f"Hey {measurement['provider']}, "
    if int(measurement[direction]) < expected:
        complain_text += (f"I was promised {expected} Mbps in {direction}load speed but "
                          f"today I have {measurement[direction]} Mbps!")
        bot.tweet_at_provider(complain_text)

make_complaint('down', PROMISED_DOWN)
make_complaint('up', PROMISED_UP)
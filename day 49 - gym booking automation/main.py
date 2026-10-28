import os
import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

ACCOUNT_NAME = "myname"
ACCOUNT_EMAIL = "myemail@test.com"
ACCOUNT_PASSWORD = "cheese"
GYM_URL = "https://appbrewery.github.io/gym/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument("--start-maximized")


def retry(func, retries=5, description=None):
    while retries:
        try:
            return func()
        except TimeoutException:
            driver.refresh()
            time.sleep(1)
            retries -= 1
    raise

def login():
    # wait loging page to load
    wait.until(ec.presence_of_element_located((By.ID, "login-page")))
    # fill info
    email_input = driver.find_element(By.ID, value="email-input")
    email_input.send_keys(ACCOUNT_EMAIL)
    pass_input = driver.find_element(By.ID, value="password-input")
    pass_input.send_keys(ACCOUNT_PASSWORD)
    submit_button = driver.find_element(By.ID, value="submit-button")
    submit_button.click()
    # wait next page to load
    wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))


driver = webdriver.Chrome(options=chrome_options)
driver.get(GYM_URL)
wait = WebDriverWait(driver, timeout=2)

# log in
login_button = driver.find_element(By.ID, value="login-button")
login_button.click()
retry(login)

# find next Tuesday 6pm class
next_tuesday_group = driver.find_element(By.CSS_SELECTOR, value="div[id*='tue']")
class_cards = next_tuesday_group.find_elements(By.CSS_SELECTOR, value="div[id$='1800'")  # 6 pm
# find all next Thursday classes
next_thursday_group = driver.find_element(By.CSS_SELECTOR, value="div[id*='thu']")
class_cards += next_thursday_group.find_elements(By.CSS_SELECTOR, value="div[id$='1800'")  # 6 pm

# counters for summary
booked_now = 0
waitlists_joined_now = 0
already_booked = 0
total_processed = booked_now + waitlists_joined_now + already_booked

print("")
for class_card in class_cards:
    class_info = class_card.text.split("\n")
    class_name = class_info[0]
    class_time = class_info[1]
    card_group = class_card.find_element(By.XPATH, value="./ancestor::div[contains(@id, 'day-group-')]")
    class_day = card_group.text.split("\n")[0]

    # click book/join waitlist
    book_button = class_card.find_element(By.CSS_SELECTOR, value="button[id^='book-button']")
    book_button_text = book_button.text
    # need to scroll properly otherwise the logout button covers the book button
    driver.execute_script("arguments[0].scrollIntoView();", book_button)
    driver.execute_script("window.scrollBy(0, -1000);")
    book_button.click()

    # print success message
    success_msg = ""
    if book_button_text == "Book Class":
        success_msg = "Booked"
        booked_now += 1
    elif book_button_text == "Join Waitlist":
        success_msg = "Joined waitlist for"
        waitlists_joined_now += 1
    elif book_button_text == "Booked":
        success_msg = "Already booked"
        already_booked += 1
    elif book_button_text == "Waitlisted":
        success_msg = "Already on waitlist"
        already_booked += 1
    print(f"{success_msg}: {class_name} on {class_day}")

# print booking summary
summary = (f"\n--- BOOKING SUMMARY ---\n"
           f"New bookings: {booked_now}\n"
           f"New waitlist entries: {waitlists_joined_now}\n"
           f"Already booked/waitlisted: {already_booked}\n"
           f"Total Tuesday and Thursday 6pm classes: {total_processed}")
print(summary)

# driver.quit()


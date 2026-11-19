from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# keep chrome open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")  # search bar does not appear if window not maximised

url = "https://en.wikipedia.org/wiki/Main_Page"

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

article_count_data = driver.find_elements(By.CSS_SELECTOR, value="#articlecount a")
article_count = article_count_data[1]

# find element by link text
all_portals = driver.find_element(By.LINK_TEXT, value="Content portals")

# find search bar
search_bar = driver.find_element(By.NAME, value="search")

# send keyboard input to search bar
search_bar.send_keys("Python", Keys.ENTER)

url = "https://appbrewery.github.io/fake-newsletter-signup/"
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

first_name_input = driver.find_element(By.NAME, value="fName")
last_name_input = driver.find_element(By.NAME, value="lName")
email_input = driver.find_element(By.NAME, value="email")

first_name_input.send_keys("First Name")
last_name_input.send_keys("Last Name")
email_input.send_keys("Email@Address.com")

signup_button = driver.find_element(By.CSS_SELECTOR, value="form button")
signup_button.click()

# driver.quit()
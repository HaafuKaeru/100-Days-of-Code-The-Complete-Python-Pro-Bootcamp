from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By

import time


# keep chrome open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")  # search bar does not appear if window not maximised


url = "https://ozh.github.io/cookieclicker/"

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
driver.implicitly_wait(2)

# login in english
english_button = driver.find_element(By.ID, value="langSelect-EN")
english_button.click()

check_intervals = 5
challenge_duration = 300

start = int(time.time())
elapsed = 0
shop_checked = False
while elapsed < challenge_duration:
    elapsed = int(time.time()) - start

    # keep clicking cookie
    try:
        big_cookie = driver.find_element(By.ID, value="bigCookie")
        big_cookie.click()
    except StaleElementReferenceException as e:
        continue

    # check shop only once every {check_intervals} seconds
    if elapsed > 0 and elapsed % check_intervals == 0:
        if not shop_checked:
            unlocked_products = driver.find_elements(By.CSS_SELECTOR, value=".product.unlocked.enabled")
            if unlocked_products:
                highest_price = 0
                highest_product = None
                for product in unlocked_products:
                    price = int(product.find_element(By.CLASS_NAME, value="price").text.replace(",", ""))
                    highest_price = max(highest_price, price)
                    if price == highest_price:
                        highest_product = product
                # buy the highest price product
                highest_product.click()
            shop_checked = True
    else:
        shop_checked = False

# print challenge score
cookies_per_second = driver.find_element(By.ID, value="cookiesPerSecond")
cookies_per_second = float(cookies_per_second.text.split()[-1])
total_cookies = driver.find_element(By.ID, value="cookies")
total_cookies = int(total_cookies.text.split()[0])

print("")
print(f"Elapsed time: {elapsed} seconds\n"
      f"Total cookies collected: {total_cookies}\n"
      f"Cookies per second: {cookies_per_second}")

driver.quit()
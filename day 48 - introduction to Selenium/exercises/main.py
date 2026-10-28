from selenium import webdriver
from selenium.webdriver.common.by import By


# keep chrome open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://www.amazon.com/Instant-Pot-Electric-Sterilizer-Stainless/dp/B09MZTP44L?nsdOptOutParam=true")
# driver.get("https://appbrewery.github.io/instant_pot/")
driver.get("https://www.python.org")

# price_dollar = driver.find_element(By.CLASS_NAME, value="a-price-whole")
# price_cents = driver.find_element(By.CLASS_NAME, value="a-price-fraction")
# print(f"The price is {price_dollar.text}.{price_cents.text}")

# search_bar = driver.find_element(By.NAME, value="q")
# print(search_bar.get_attribute("placeholder"))
# button = driver.find_element(By.ID, value="submit")
# print(button.size)
# documentation_link = driver.find_element(By.CSS_SELECTOR, value=".documentation-widget a")
# print(documentation_link.text)

# bug_link = driver.find_element(By.XPATH, value='/html/body/div/footer/div[2]/div/ul/li[3]/a')
# print(bug_link.text)


event_times = driver.find_elements(By.CSS_SELECTOR, value=".event-widget time")
event_names = driver.find_elements(By.CSS_SELECTOR, value=".event-widget li a")
events_dict = {i: {'time': event_times[i].text, 'name': event_names[i].text} for i in range(len(event_times))}
print(events_dict)



# driver.close()
driver.quit()
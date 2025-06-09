from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
query = "lip gloss"
driver.get(f"https://www.nykaa.com/makeup/lips/{query}/c/250?search_redirection=True")

elem = driver.find_element(By.CLASS_NAME, "css-d5z3ro")

print(elem.get_attribute("outerHTML"))  # Print the href attribute of the element
time.sleep(5)  # Wait for a few seconds to see the results
driver.close()
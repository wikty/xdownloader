import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import config


driver = webdriver.Firefox(executable_path=config.GECKO_DRIVER_PATH)
# WebDriver will wait until the page has 
# fully loaded (that is, the “onload” event has fired)
driver.get("http://www.python.org")
assert "Python" in driver.title
# Find element by its name attribute
elem = driver.find_element_by_name("q")
elem.clear()
# Send keys, this is similar to entering keys using your keyboard.
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
# The quit will exit entire browser whereas close` will close one tab, but if just one tab was open
# driver.quit()
# driver.close()
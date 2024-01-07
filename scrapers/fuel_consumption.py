from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from conversions import wait_for_a_second


car_data = {
    # car brand
    # car model
    # car year
    # car engine capacity
    # car fuel type
    # car engine power
}

driver = webdriver.Chrome()

# the url of the fuel consumption website
# huge database of user records about thier vehicle's fuel consumption
url = "https://www.spritmonitor.de/en/search.html"

wait_for_a_second(1)
driver.get(url)

# deal with the cookies pop up window
try:
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if button.text == "Einwilligen" or button.text == "Consent":
            button.click()
            break
    else:
        raise Exception
except Exception as e:
    print(e)
    pass

stop = 0

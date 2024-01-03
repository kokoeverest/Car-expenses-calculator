from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from conversions import (
    wait_for_a_second,
    convert_car_string 
)
"""This scraper chould accept the car object and add the tires sizes and prices to the calculations"""


# the car_data dict should be 
# {"makers": convert_car_string(car.brand),
#  "models": convert_car_string(car.model),
#  "years": car.year}

car_data = {
    'makers': 'dacia', 
    'models': 'duster',
    'years': "2012"
}

driver = webdriver.Chrome()

# the url of the Car tires calculator
url = "https://www.bggumi.com/"

# just an artificial pause
wait_for_a_second(1)

# load the page contents with the Selenium webdriver 
# (the site uses JS scripts to handle the form submission)
driver.get(url)

error = False

for k, v in car_data.items():
    try:
        el = driver.find_element(By.XPATH, f"//option[@value='{v}']").click()
    except Exception as e:
        error = True

# if there's an error, the button will not be clickable. Maybe raise error or skip the calculation of the tire's price?
if not error:
    button = driver.find_element(By.ID, 'get_wheelsize').click()

# next: get the minimum and maximum tires prices depending on the car engine and results

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from conversions import wait_for_a_second, convert_car_string
import sys
sys.path.append('.')
from models.tire import Tire
from datetime import datetime
"""This scraper should accept the car object and add the tires sizes and prices to the calculations"""

def add_product_price():
    """Get the price of the first found product"""
    product = driver.find_element(By.CLASS_NAME, "price").text
    try:
        matches = re.findall(r"^\d+,\d+|^\d+\.\d+|^\d+", product)
        if len(matches) > 0:
            product = matches[0]
        return float(product)
    except:
        try:
            # if the price of one tire is ridiculously high, above 1000 leva, it will be separated by a comma
            product = product.replace(",", "") 
            return float(product)
        except:
            return
            

start = datetime.now()
print("Start: ", start)
# the car_data dict should be 
# {"makers": convert_car_string(car.brand),
#  "models": convert_car_string(car.model),
#  "years": car.year}

car_data = {
    'makers': 'subaru', 
    'models': 'outback',
    'years': "2012"
}
engine_data = {
    "capacity": "1.5",
    "power_hp": "1.5 dCi 110HP"
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
exc = None
for k, v in car_data.items():
    try:
        el = driver.find_element(By.XPATH, f"//option[@value='{v}']").click()
        wait_for_a_second(2) # use the WebDriverWait would be much better than artificial pauses
    except Exception as e:
        error = True
        exc = e
# if there's an error, the button will not be clickable. Maybe raise error or skip the calculation of the tire's price?
if not error:
    button = driver.find_element(By.ID, 'get_wheelsize').click()
else:
    print(str(exc))
    raise SystemExit(str(exc))

# get the minimum and maximum tires prices depending on the car engine and results
pattern = r"\d{3}/\d{2}R\d{2}|\d{3}/\d{2}ZR\d{2}"

wait_for_a_second(1)

# find the possible tires sizes in the resulting table
possible_tire_sizes = set()
table_rows = driver.find_elements(By.TAG_NAME, "tr")

for row in table_rows:
    matches = re.findall(pattern, row.text)
    if len(matches) > 0: possible_tire_sizes.add(*matches)


# collect only the min and max_price for every possible tire size
tires = []
for size in possible_tire_sizes:
    w, h, i = size[:3], size[4:6], size[-2:]
    link_url = f"eshop/search?type=1&width={w}&height={h}&inch={i}"
    
    driver.get(url + link_url)
    tire = Tire(width=w, height=h, size=i)
    
    tire.min_price = add_product_price()

    sort_products = Select(driver.find_element(By.ID, "sortby")).select_by_value("2")
    wait_for_a_second(1)

    tire.max_price = add_product_price()
    tires.append(tire)

print([[tire.min_price, tire.max_price, tire] for tire in tires])
print(datetime.now(), "Duration: ", datetime.now() - start) # around 40 seconds without using waits
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from conversions import (
    wait_for_a_second, 
    age_convertor, 
    calculate_euro_catagory,
    hp_to_kw_converter)



def extract_option_or_input_fields(elem, value, field_name="option"):
    options = elem.find_elements(By.TAG_NAME, field_name)
    result = []
    for option in options:
        result.append(option.text)
        opt_value = option.get_attribute("value")
        if opt_value == value and field_name == "option":
            option.click()
    return set(result)

car_tax_data = {
    'obl': 'София', # should be "obl": car.tax.city
    'obs': 'Столична', # should be "obs": car.tax.municipality
    'old': age_convertor("2012"), # should be "old": car.year 
    'euro': calculate_euro_catagory("Euro 3"), # should be "euro": car.engine.emissions_category
    'kw': hp_to_kw_converter("136") # # should be "kw": car.engine.power (if the power is not in kw - use the convertor)
}

driver = webdriver.Chrome()

# the url of the Car taxes calculator for the territory of Bulgaria
url = "https://cartax.uslugi.io/"

# just an artificial pause
wait_for_a_second(1)

# load the page contents with the Selenium webdriver 
# (the site uses JS scripts to handle the form submission)
driver.get(url)

# locate the input fields of the form 
# for this website there are 5 input fields, as defined in the car_data dict
all_options = {}
for k, v in car_tax_data.items():
    try:
        el = driver.find_element(By.XPATH, f"//select[@name='{k}']")
        all_options[k] = extract_option_or_input_fields(el, v)
    except Exception as e:
            # the 'kw' input field
        try:
            el = driver.find_element(By.XPATH, f"//input[@name='{k}']")
            all_options[k] = extract_option_or_input_fields(el, v, field_name="input")
            el.clear()
            el.send_keys(v)
            el.submit()
        except Exception as e:
            continue

result = driver.find_element(By.CLASS_NAME, "amount").text

print(result) # def get_price_as_float

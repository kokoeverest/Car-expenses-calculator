import os
import pickle
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
sys.path.append('.')
from scrapers.conversions import (
    age_convertor, 
    calculate_euro_category,
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

def start_driver():
    driver = webdriver.Chrome()
    url = "https://cartax.uslugi.io/"
    driver.get(url)
    return driver

def generate_car_data_dict(
        city: str,
        municipality: str,
        age: str,
        euro: str,
        power: int
        ):
    lst = [city, municipality, age_convertor(age), calculate_euro_category(euro), hp_to_kw_converter(power)]
    data = ['obl', 'obs', 'old', 'euro', 'kw']

    return dict(el for el in zip(data, lst))

def get_tax_price(car_data: list):
    car_data_dict = generate_car_data_dict(*car_data)
    json_data = json.dumps(car_data_dict, indent=2, ensure_ascii=False, separators=('', ' - '))
    cwd = os.getcwd()
    
    with open(cwd+"/taxes.txt", "rb") as file:
        try:
            tax_price = pickle.load(file)
            return tax_price[json_data]
        except EOFError:
            tax_price = {}
        except KeyError:
            tax_price = tax_price # type: ignore

    driver = start_driver()
    all_options = {}
    for k, v in car_data_dict.items():
        try:
            el = driver.find_element(By.XPATH, f"//select[@name='{k}']")
            all_options[k] = extract_option_or_input_fields(el, v)
        except:
                # the 'kw' input field
            try:
                el = driver.find_element(By.XPATH, f"//input[@name='{k}']")
                all_options[k] = extract_option_or_input_fields(el, v, field_name="input")
                el.clear()
                el.send_keys(v)
                el.submit()
            except:
                continue
    try:
        price = driver.find_element(By.CLASS_NAME, "amount").text.split(' ')[0]
    except IndexError:
        price = '0'

    tax_price[json_data] = price

    with open(cwd+"/taxes.txt", "wb") as file:
        pickle.dump(tax_price, file)

    return price
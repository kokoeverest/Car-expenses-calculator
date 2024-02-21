from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pickle
import os
import re
import sys
sys.path.append('.')
from models.tire import Tire
from scrapers.conversions import wait_for_a_second, convert_car_string


"""This scraper should accept the car object and add the tires sizes and prices to the calculations"""


def find_tire_sizes(driver):
    pattern = r"\d{3}/\d{2}R\d{2}|\d{3}/\d{2}ZR\d{2}"
    possible_tire_sizes = set()
    wait_for_a_second()
    table_rows = driver.find_elements(By.TAG_NAME, "tr")

    for row in table_rows[1:]:
        matches = re.findall(pattern, row.text)
        if len(matches) > 0: 
            possible_tire_sizes.add(*matches)

    return possible_tire_sizes


def collect_tires_prices(tire_sizes: set|list, driver):
    url = "https://www.bggumi.com/"
    tires = []
    for size in tire_sizes:
        w, h, i = size[:3], size[4:6], size[-2:]
        link_url = f"eshop/search?type=1&width={w}&height={h}&inch={i}"
        
        wait_for_a_second()
        # tires are sorted by lowest price by default
        driver.get(url + link_url)
        tire = Tire(width=w, height=h, size=i)
        tire.min_price = add_product_price(driver)

        wait_for_a_second()
        # sort tires by highest price first
        Select(driver.find_element(By.ID, "sortby")).select_by_value("2")
        tire.max_price = add_product_price(driver)
        tires.append(tire)
    return tires


def add_product_price(driver):
    """Get the price of the first found product"""
    wait_for_a_second(1)
    
    try: 
        product = driver.find_element(By.CLASS_NAME, "price").text
    except Exception: 
        return
    
    try:
        matches = re.findall(r"^\d+,\d+|^\d+\.\d+|^\d+", product)
        if len(matches) > 0:
            product = matches[0]
            return float(product)
    except Exception:
        try:
            # if the price of one tire is ridiculously high, above 1000 leva, it will be separated by a comma
            product = product.replace(",", "") 
            return float(product)
        except Exception:
            return


def start_driver():
    url = "https://www.bggumi.com/"
    driver = webdriver.Chrome()
    wait_for_a_second(1)
    driver.get(url)

    return driver 


def get_tires_prices(search: list):
    search = [convert_car_string(el) for el in search]
    cwd = os.getcwd()
    driver = None
    # looking for the tire sizes of the car brand, model and year in the file
    with open(cwd+"/car_tires.txt", "rb") as file:
        try:
            data: dict[dict, dict[dict, dict[str, list]]] = pickle.load(file)
        except EOFError:
            data = {}
    all_tire_sizes = set()
    brand, model, year = search
    try:
        possible_sizes = data[brand][model][year]
    except KeyError:
        possible_sizes = []
        
    if len(possible_sizes) == 0:
        driver = start_driver()
        Select(driver.find_element(By.ID, "makers")).select_by_value(brand)
        wait_for_a_second()
        Select(driver.find_element(By.ID, "models")).select_by_value(model)
        wait_for_a_second()
        Select(driver.find_element(By.ID, "years")).select_by_value(year)
        wait_for_a_second()
        button = driver.find_element(By.ID, 'get_wheelsize')
        wait_for_a_second(1)
        button.click()

        possible_sizes = find_tire_sizes(driver)
        if len(possible_sizes) > 0:
            all_tire_sizes.update(possible_sizes)

        if brand not in data.keys(): 
            data[brand] = {}
        if model not in data[brand]:
            data[brand][model] = {}
        if year not in data[brand][model]:
            data[brand][model][year] = []
        data[brand][model][year] = list(possible_sizes)

        # write the new car data to the file
        with open(cwd+"/car_tires.txt", "wb") as file:
            pickle.dump(data, file)

    # then look for the price of each tire in the file
    with open(os.getcwd()+"/tires_prices_final.txt", "rb") as sizes_file:
        try:
            existing_sizes: dict = pickle.load(sizes_file)
        except EOFError:
            existing_sizes = {}

    final_result = []
    if len(existing_sizes) > 0:
        for tire in possible_sizes:
            if tire in existing_sizes:
                final_result.append(existing_sizes.get(tire))

    #if there are missing tires in the file - scrape them and update the file with the prices for each tire
    if len(final_result) == 0:
        if not driver: 
            driver = start_driver()
        final_result = collect_tires_prices(possible_sizes, driver)
        for tire in possible_sizes:
            try:
                res = collect_tires_prices([tire], driver)
                existing_sizes[str(tire)] = next(iter(res), None)
            except Exception:
                continue
        with open(os.getcwd()+"/tires_prices_final.txt", "wb") as file3:
            pickle.dump(existing_sizes, file3)
    if driver:
        driver.close()

    return final_result
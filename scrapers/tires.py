from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from datetime import datetime
import pickle
import os
import re
import sys
sys.path.append('.')
from models.tire import Tire
from conversions import wait_for_a_second, convert_car_string
"""This scraper should accept the car object and add the tires sizes and prices to the calculations"""


def find_tire_sizes():
    pattern = r"\d{3}/\d{2}R\d{2}|\d{3}/\d{2}ZR\d{2}"
    possible_tire_sizes = set()
    wait_for_a_second(1)
    table_rows = driver.find_elements(By.TAG_NAME, "tr")

    for row in table_rows[1:]:
        matches = re.findall(pattern, row.text)
        if len(matches) > 0: 
            possible_tire_sizes.add(*matches)

    return possible_tire_sizes


def collect_tires_prices(tire_sizes: set):
    tires = []
    for size in tire_sizes:
        w, h, i = size[:3], size[4:6], size[-2:]
        link_url = f"eshop/search?type=1&width={w}&height={h}&inch={i}"
        
        wait_for_a_second(1)
        # tires are sorted by lowest price by default
        driver.get(url + link_url)
        tire = Tire(width=w, height=h, size=i)
        tire.min_price = add_product_price()

        wait_for_a_second(1)
        # sort tires by highest price first
        Select(driver.find_element(By.ID, "sortby")).select_by_value("2")
        tire.max_price = add_product_price()
        tires.append(tire)
    return tires

def add_product_price():
    """Get the price of the first found product"""
    wait_for_a_second(1)
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


def select_car_brands_and_models():
    all_tire_sizes = set()
    select_brands = Select(driver.find_element(By.ID, "makers"))
    all_car_brands = [option.get_attribute("value") 
                      for option in select_brands.options]
    if all_car_brands[0] == "": 
        all_car_brands.pop(0)
    wait_for_a_second(1)

    for brand in all_car_brands:
         
        # if brand != "audi":
        #     continue
    
        if brand is not None: 
            brand = convert_car_string(brand)
            Select(driver.find_element(By.ID, "makers")).select_by_value(brand)
        try:
            wait_for_a_second(3)
            select_models = Select(driver.find_element(By.ID, "models"))
            current_models = [option.get_attribute("value") for option in select_models.options]
            if current_models[0] == "": 
                current_models.pop(0)

            for model in current_models:
                if model is not None: 
                    Select(driver.find_element(By.ID, "models")).select_by_value(model)
                try:
                    wait_for_a_second()
                    select_years = Select(driver.find_element(By.ID, "years"))
                    current_years = [option.get_attribute("value") for option in select_years.options]
                    if current_years[0] == "": 
                        current_years.pop(0)

                    for year in current_years:
                        if year is not None:
                            Select(driver.find_element(By.ID, "years")).select_by_value(year)
                        wait_for_a_second(2)
                        driver.find_element(By.ID, 'get_wheelsize').click()
                        
                        possible_sizes = find_tire_sizes()
                        if len(possible_sizes) > 0:
                            all_tire_sizes.update(possible_sizes)
                        # if len(possible_sizes) > 0:
                        #     wait_for_a_second()
                        #     current_tires_prices = collect_tires_prices(possible_sizes)
                        # else:
                        #     current_tires_prices = []

                        if brand not in all_cars_dict: 
                            all_cars_dict[brand] = {}
                        if model not in all_cars_dict[brand]:
                            all_cars_dict[brand][model] = {}
                        if year not in all_cars_dict[brand][model]:
                            # all_cars_dict[brand][model][year] = current_tires_prices
                            all_cars_dict[brand][model][year] = list(possible_sizes)
                        
                        cwd = os.getcwd()
                        with open(cwd+"/car_tires2.txt", "wb") as file:
                            pickle.dump(all_cars_dict, file)

                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print(e)
            continue

    return all_cars_dict




start = datetime.now()
print("Start: ", start)
# the car_data dict should be 
# {"makers": convert_car_string(car.brand),
#  "models": convert_car_string(car.model),
#  "years": car.year}

car_data = {
    'makers': 'audi', 
    'models': 'a4',
    'years': "2015"
}

driver = webdriver.Chrome()
driver.implicitly_wait(10)

# the url of the Car tires calculator
url = "https://www.bggumi.com/"

# just an artificial pause
wait_for_a_second(1)

# load the page contents with the Selenium webdriver 
# (the site uses JS scripts to handle the form submission)
driver.get(url)

with open("/home/kaloyan/web_scraper/Projects/car_tires2.txt", "rb") as file:
        try:
            all_cars_dict = pickle.load(file)
        except EOFError:
            all_cars_dict = {}
all_cars_dict = select_car_brands_and_models()

stop_here = True
# ------------------------------------------------------
def execute():
    error = False
    exc = None
    for k, v in car_data.items():
        try:
            el = driver.find_element(By.XPATH, f"//option[@value='{v}']").click()  
            wait_for_a_second() # use the WebDriverWait would be much better than artificial pauses
        except Exception as e:
            error = True
            exc = e
    # if there's an error, the button will not be clickable. Maybe raise error or skip the calculation of the tire's price?
    if not error:
        button = driver.find_element(By.ID, 'get_wheelsize').click()
    else:
        print(exc, "at:", datetime.now())
        raise SystemExit(str(exc))

# get the minimum and maximum tires prices depending on the car engine and results


wait_for_a_second(1)

# find the possible tires sizes in the resulting table
possible_tire_sizes = find_tire_sizes()

# collect only the min and max_price for every possible tire size
tires: list[Tire] = collect_tires_prices(possible_tire_sizes)

print([[f"{tire.min_price} лв, {tire.max_price} лв", tire] for tire in tires])
print(datetime.now(), "Duration: ", datetime.now() - start) # around 40 seconds without using waits
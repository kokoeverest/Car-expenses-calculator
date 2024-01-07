# from bs4 import BeautifulSoup as bs
# from urllib.request import urlopen
# import requests
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.select import Select
# from datetime import datetime
# import pickle
# import os
# import re
# import sys
# sys.path.append('.')
# from models.tire import Tire
# from conversions import wait_for_a_second, convert_car_string
# """This scraper should accept the car object and add the tires sizes and prices to the calculations"""

# def add_product_price():
#     """Get the price of the first found product"""
#     product = driver.find_element(By.CLASS_NAME, "price").text
#     try:
#         matches = re.findall(r"^\d+,\d+|^\d+\.\d+|^\d+", product)
#         if len(matches) > 0:
#             product = matches[0]
#             return float(product)
#     except:
#         try:
#             # if the price of one tire is ridiculously high, above 1000 leva, it will be separated by a comma
#             product = product.replace(",", "") 
#             return float(product)
#         except:
#             return

# def execute(car_data: dict):
#     error = False
#     exc = None
#     for k, v in car_data.items():
#         try:
#             if k == "years":
#                 year = next(iter(car_data["years"]))
#             el = driver.find_element(By.XPATH, f"//option[@value='{v}']").click()  
#             wait_for_a_second() # use the WebDriverWait would be much better than artificial pauses
#         except Exception as e:
#             error = True
#             exc = e
#     # if there's an error, the button will not be clickable. Maybe raise error or skip the calculation of the tire's price?
#     if not error:
#         button = driver.find_element(By.ID, 'get_wheelsize').click()
#     else:
#         print(exc, "at:", datetime.now())
#         exit(1)


# def select_car_brands_and_models():
#     current_cars_data = {"makers": "", "models": "", "years": ""}
#     select_brands = driver.find_element(By.ID, "makers")
#     all_car_brands = select_brands.text.split("\n")
#     wait_for_a_second()
#     all_car_brands.pop(0)
#     # current_cars_data["makers"] = all_car_brands
#     for brand in all_car_brands:
#         brand = convert_car_string(brand)
#         if brand != "audi":
#             continue
#         current_cars_data["makers"] = brand
#         driver.find_element(By.XPATH, f"//option[@value='{brand}']").click()
#         wait_for_a_second()
        
#         try:
#             select_models = driver.find_element(By.ID, "models")
#             current_models = select_models.text.split("\n")
#             current_models.pop(0)
#             for model in current_models:
#                 current_cars_data["models"] = model
#                 current_cars_data["years"] = "2020"

#                 execute(current_cars_data)
#                 # el = driver.find_element(By.XPATH, f"//option[@value='{model}']").click
#                 # wait_for_a_second(4)
#                 # try:
#                 #     select_years = driver.find_element(By.ID, "years")
#                 #     current_years = select_years.text.split("\n")
#                 #     current_years.pop(0) 
#                 #     for year in current_years:
#                 #         year_button = driver.find_element(By.XPATH, f"//option[@value='{year}']").click()
                        
#                 #         get_wheelsize_button = driver.find_element(By.ID, 'get_wheelsize').click()

#                 #         possible_sizes = find_tire_sizes()
#                 #         if len(possible_sizes) > 0:
#                 #             # wait_for_a_second()
#                 #             current_tires_prices = collect_tires_prices(possible_sizes)
#                 #         else:
#                 #             current_tires_prices = []

#                 #         if brand not in all_cars_dict: 
#                 #             all_cars_dict[brand] = {}
#                 #         if model not in all_cars_dict[brand]:
#                 #             all_cars_dict[brand][model] = {}
#                 #         if year not in all_cars_dict[brand][model]:
#                 #             all_cars_dict[brand][model][year] = current_tires_prices
                        
#                 #         cwd = os.getcwd()
#                 #         with open(cwd+"/car_tires.txt", "wb") as file:
#                 #             pickle.dump(all_cars_dict, file)

#                 #     driver.refresh()
#                 # except Exception as e:
#                 #     print(e)
#                 #     continue
#         except Exception as e:
#             print(e)
#             continue

#     return all_cars_dict


# def find_tire_sizes():
#     pattern = r"\d{3}/\d{2}R\d{2}|\d{3}/\d{2}ZR\d{2}"
#     possible_tire_sizes = set()
#     table_rows = driver.find_elements(By.TAG_NAME, "tr")

#     for row in table_rows[1:]:
#         matches = re.findall(pattern, row.text)
#         if len(matches) > 0: 
#             possible_tire_sizes.add(*matches)
#     return possible_tire_sizes


# def collect_tires_prices(tire_sizes: set):
#     tires = []
#     for size in tire_sizes:
#         w, h, i = size[:3], size[4:6], size[-2:]
#         link_url = f"eshop/search?type=1&width={w}&height={h}&inch={i}"
        
#         # tires are sorted by lowest price by default
#         driver.get(url + link_url)
#         tire = Tire(width=w, height=h, size=i)
#         tire.min_price = add_product_price()

#         wait_for_a_second()
#         # sort tires by highest price first
#         sort_products = Select(driver.find_element(By.ID, "sortby")).select_by_value("2")
#         tire.max_price = add_product_price()
#         tires.append(tire)
#     return tires


# start = datetime.now()
# print("Start: ", start)
# # the car_data dict should be 
# # {"makers": convert_car_string(car.brand),
# #  "models": convert_car_string(car.model),
# #  "years": car.year}

# car_data = {
#     'makers': 'audi', 
#     'models': 'a4',
#     'years': ["1920", "2000", "2020"]
# }

# driver = webdriver.Chrome()

# # the url of the Car tires calculator
# url = "https://www.bggumi.com/"

# # just an artificial pause
# wait_for_a_second(1)

# # load the page contents with the Selenium webdriver 
# # (the site uses JS scripts to handle the form submission)
# driver.get(url)

# with open("/home/kaloyan/web_scraper/Projects/car_tires.txt", "rb") as file:
#         try:
#             all_cars_dict = pickle.load(file)
#         except EOFError:
#             all_cars_dict = {}
# # all_cars_dict = select_car_brands_and_models()

# stop_here = True
# # ------------------------------------------------------

# # get the minimum and maximum tires prices depending on the car engine and results

# execute(car_data)
# wait_for_a_second(1)

# # find the possible tires sizes in the resulting table
# possible_tire_sizes = find_tire_sizes()

# # collect only the min and max_price for every possible tire size
# tires: list[Tire] = collect_tires_prices(possible_tire_sizes)

# print([[f"{tire.min_price} лв, {tire.max_price} лв", tire] for tire in tires])
# print(datetime.now(), "Duration: ", datetime.now() - start) # around 40 seconds without using waits


# -------------------------------------------------------------
from datetime import datetime
import pickle
import sys
sys.path.append('.')
from models.tire import Tire

start = datetime.now()
with open("/home/kaloyan/web_scraper/Projects/car_tires.txt", "rb") as file:
    try:
        data: dict[dict, dict[dict, dict[str, list]]] = pickle.load(file)
    except EOFError:
        data = {}

all_tires = []
distinct_tires = set()

for brand, model in data.items():
    for m_name, year in model.items():
        for y_value, tires in year.items():
            for tire in tires:
                all_tires.append(str(tire))
                distinct_tires.add(str(tire))

end = datetime.now()
diff = (end - start).microseconds
print(f"Duration: {diff}")
print(f'all tires: {len(all_tires)}', f"distinct: {len(distinct_tires)}")

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
    tires = []
    for size in tire_sizes:
        w, h, i = size[:3], size[4:6], size[-2:]
        link_url = f"eshop/search?type=1&width={w}&height={h}&inch={i}"
        
        wait_for_a_second(1)
        # tires are sorted by lowest price by default
        driver.get(url + link_url)
        tire = Tire(width=w, height=h, size=i)
        tire.min_price = add_product_price(driver)

        wait_for_a_second(1)
        # sort tires by highest price first
        Select(driver.find_element(By.ID, "sortby")).select_by_value("2")
        tire.max_price = add_product_price(driver)
        tires.append(tire)
    return tires

def add_product_price(driver):
    """Get the price of the first found product"""
    wait_for_a_second(1)
    
    try: product = driver.find_element(By.CLASS_NAME, "price").text
    except: return
    
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

# collect the tire sizes into a file - the existing records should be ignored 
# in the next call of this process, because it is veeeery slow
# 
# commented in order to manually update the prices
# uncomment to start scraping for new tire sizes
def select_car_brands_and_models():

    with open("/home/kaloyan/web_scraper/Projects/car_tires.txt", "rb") as file:
        try:
            all_cars_dict = pickle.load(file)
        except EOFError:
            all_cars_dict = {}
    cwd = os.getcwd()
    driver = start_driver()
    all_tire_sizes = set()
    # select_brands = Select(driver.find_element(By.ID, "makers"))
    # all_car_brands = [option.get_attribute("value") 
    #                   for option in select_brands.options]
    # if all_car_brands[0] == "": 
    #     all_car_brands.pop(0)
    # wait_for_a_second(1)

    for brand, models in all_cars_dict.items():    
        if brand is not None: 
            # brand = convert_car_string(brand)
            Select(driver.find_element(By.ID, "makers")).select_by_value(brand)
        try:
            # try: 
            #     all_cars_dict[brand]
            #     continue
            # except KeyError:
            wait_for_a_second(3)
                # select_models = Select(driver.find_element(By.ID, "models"))
                # current_models = [option.get_attribute("value") for option in select_models.options]
                # if current_models[0] == "": 
                #     current_models.pop(0)

            for model, years in models.items():
                if model is not None: 
                    Select(driver.find_element(By.ID, "models")).select_by_value(model)
                try:
                    wait_for_a_second()
                #     select_years = Select(driver.find_element(By.ID, "years"))
                #     current_years = [option.get_attribute("value") for option in select_years.options]
                #     if current_years[0] == "": 
                #         current_years.pop(0)

                    for year in years:
                        if all_cars_dict[brand][model][year] == []: #list(possible_sizes)

                            if year is not None:
                                Select(driver.find_element(By.ID, "years")).select_by_value(year)
                            wait_for_a_second(1)
                            driver.find_element(By.ID, 'get_wheelsize').click()
                            
                            possible_sizes = find_tire_sizes(driver)
                            if len(possible_sizes) > 0:
                                all_tire_sizes.update(possible_sizes)

                            all_cars_dict[brand][model][year] = list(possible_sizes)
                        # if brand not in all_cars_dict: 
                        #     all_cars_dict[brand] = {}
                        # if model not in all_cars_dict[brand]:
                        #     all_cars_dict[brand][model] = {}
                        # if year not in all_cars_dict[brand][model]:
                        #     all_cars_dict[brand][model][year] = list(possible_sizes)
            
                
                except Exception:
                    with open(cwd+'/tires_missing_car_data.txt', 'a') as misiing:
                        print(f'{brand} {model} {year}', file=misiing)
                    continue
                
        except Exception:
            with open(cwd+'/tires_missing_car_data.txt', 'a') as misiing:
                print(f'{brand} {model} {year}', file=misiing)
            continue

        finally:
            with open(cwd+"/car_tires.txt", "wb") as file:
                pickle.dump(all_cars_dict, file)

    return all_cars_dict


def start_driver():
    driver = webdriver.Chrome()
    wait_for_a_second(1)
    driver.get(url)

    return driver 


def write_missing_car_data_to_file(missing: list | set, file_path: str):
    with open(os.getcwd()+file_path, "rb") as file_missing_data:
        try:
            new_data: list | set = pickle.load(file_missing_data)
        except EOFError:
            new_data = [] if isinstance(missing, list) else set()

        if isinstance(new_data, list):
            new_data.append(missing)
        else:
            new_data.update(missing)

    with open(os.getcwd()+file_path, "wb") as file:
        pickle.dump(new_data, file)


def get_tires_prices_from_file(search: list):
    search = [convert_car_string(el) for el in search]

    with open(os.getcwd()+"/tires_prices_final.txt", "rb") as sizes_file:
        try:
            existing_sizes: dict = pickle.load(sizes_file)
        except EOFError:
            existing_sizes = {}
    
    with open(os.getcwd()+"/car_tires.txt", "rb") as file:
        try:
            data: dict[dict, dict[dict, dict[str, list]]] = pickle.load(file)
        except EOFError:
            data = {}
# update the workflow -> look for the price in the file -> scrape the car data if it's missing ->
# look for the tire price in the file -> scrape it if it's missing -> pickle the updated dicts in the files
    search_result = None
    final_result = []
    missing_tire_sizes: set[str] = set()
    
    for brand, models in data.items():
        for model, years in models.items():
            for year, tires in years.items():
                if [brand, model, year] == search:
                    search_result = tires
                    break
            if search_result: break
        if search_result: break


    # if not search_result:
    #     missing_car_data = search
    #     write_missing_car_data_to_file(missing_car_data, "/missing_car_data.txt")
    # else:
    #     for tire in search_result:
    #         if tire in existing_sizes:
    #             final_result.append(existing_sizes.get(tire))
    #         else:
    #             missing_tire_sizes.add(tire)
    #     if missing_tire_sizes:
    #         write_missing_car_data_to_file(missing_tire_sizes, "/missing_tires_sizes.txt")
    
    return final_result
    

def scrape_tire_prices():
    driver = start_driver()
    with open(os.getcwd()+"/tires_prices_final.txt", "rb") as file:
        try:
            existing_sizes = pickle.load(file)
        except EOFError:
            existing_sizes = {}
    
    with open(os.getcwd()+"/car_tires.txt", "rb") as file:
        try:
            data: dict[dict, dict[dict, dict[str, list]]] = pickle.load(file)
        except EOFError:
            data = {}

    all_tires = []
    existing = []

    for _, model in data.items():
        for _, year in model.items():
            for _, tires in year.items():
                for tire in tires:
                    if tire not in all_tires: all_tires.append(tire)

    for size, tire in existing_sizes.items():
        if size not in existing: 
            existing.append(str(tire))

    missing = set(all_tires).difference(set(existing))

    for tire in missing:
        try:
            res = collect_tires_prices([tire], driver)
            existing_sizes[str(tire)] = next(iter(res), None)
            with open(os.getcwd()+"/tires_prices_final.txt", "wb") as file3:
                pickle.dump(existing_sizes, file3)
        except:
            continue


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# the main flow of the scraper (trying to get the prices from the file first)

car_data = {
    'makers': 'dacia', 
    'models': 'duster',
    'years': "2022"
}

# the url of the Car tires calculator
url = "https://www.bggumi.com/"
# result = get_tires_prices_from_file(list(car_data.values()))

# min_price = min(tire.min_price for tire in result) if result else None
# max_price = max(tire.max_price for tire in result) if result else None
# print(
#     f"Tires for " 
#     f"{car_data['makers'].capitalize()} "
#     f"{car_data['models'].capitalize()} "
#     f"{car_data['years']}:\n"
#     f"Lowest price:  {min_price} leva\n"
#     f"Highest price: {max_price} leva")

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''
 ------------------------------------------------------------------
 scrape for car tires data 
 (should be called manually to update all the car models with their tire sizes)
 the execution of this scraping takes very long time, so concider running it during the night

 ------------------------------------------------------------------
'''
select_car_brands_and_models()

# __________________________________________________________________
# after scraping for the cars data now execute this function to collect the prices of the tires
# this process is also quite slow

# scrape_tire_prices()
# print("Finished scraping tire sizes:", datetime.now())
# __________________________________________________________________
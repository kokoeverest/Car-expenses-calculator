import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from scrapers.conversions import wait_for_a_second, price_convertor, find_correct_name
import sys
sys.path.append('.')


def find_fuel_consumption(
        brand: str, 
        model: str, 
        year_from: str, 
        year_to: str, 
        fuel_type: str, 
        power_from: str, 
        power_to: str,
        avg_consumption = '0'
    ):
    wait_for_a_second(1)
    driver = start_driver()
    brand = find_correct_name(brand, {opt.text for opt in Select(driver.find_element(By.ID, "manuf")).options})
    if brand != "":
        Select(driver.find_element(By.ID, "manuf")).select_by_visible_text(brand)
    wait_for_a_second(1)
    try:
        model = find_correct_name(model, {opt.text for opt in Select(driver.find_element(By.ID, "model")).options})
        if model != "":
            Select(driver.find_element(By.ID, "model")).select_by_visible_text(model)
        Select(driver.find_element(By.ID, "fueltype")).select_by_visible_text(fuel_type.capitalize())
        driver.find_element(By.ID, "constyear_s").send_keys(year_from)
        driver.find_element(By.ID, "constyear_e").send_keys(year_to)
        driver.find_element(By.ID, "power_s").send_keys(int(power_from) - 10)
        driver.find_element(By.ID, "power_e").send_keys(int(power_to) + 10)
        driver.find_element(By.XPATH, "//*[@id='add']").submit()
        wait_for_a_second()
        avg_consumption = driver.find_element(By.CLASS_NAME, "consumption").text            
    except Exception as e:
        print(e)
        
    return avg_consumption


def start_driver():
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
            raise Exception("Consent button was not found")
    except Exception as e:
        print(str(e))
        pass

    return driver 


def get_fuel_consumption(car_data: list[str]):
    # try to find the fuel consumption locally
    cwd = os.getcwd()
    with open(cwd+"/fuel_consumption.txt", "rb") as file:
        try:
            all_cars_dict = pickle.load(file)
        except EOFError:
            all_cars_dict = {}

    if all(car_data):
        brand, model, year_from, year_to, fuel_type, power_from, power_to = car_data
        
        try:
            avg_consumption = all_cars_dict[brand][model][fuel_type][year_to][power_to]
        except KeyError:
            avg_consumption = '0'

        # if such record does not exist, start the driver and scrape it from the website
        if avg_consumption == '0':
            avg_consumption = find_fuel_consumption(
                brand, model, year_from, year_to, fuel_type, power_from, power_to
            )
            if brand not in all_cars_dict.keys(): 
                all_cars_dict[brand] = {}
            if model not in all_cars_dict[brand]:
                all_cars_dict[brand][model] = {}
            if fuel_type not in all_cars_dict[brand][model]:
                all_cars_dict[brand][model][fuel_type] = {}
            if year_to not in all_cars_dict[brand][model][fuel_type]:
                all_cars_dict[brand][model][fuel_type][year_to] = {}
            if power_to not in all_cars_dict[brand][model][fuel_type][year_to]:
                all_cars_dict[brand][model][fuel_type][year_to][power_to] = {}
            if avg_consumption not in all_cars_dict[brand][model][fuel_type][year_to][power_to]:
                all_cars_dict[brand][model][fuel_type][year_to][power_to] = avg_consumption
            
            with open(cwd+"/fuel_consumption.txt", "wb") as file:
                pickle.dump(all_cars_dict, file)    
    else:
        avg_consumption = '0'
    return price_convertor(avg_consumption) 

import os
import pickle
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from scrapers.conversions import (
    wait_for_a_second, 
    price_convertor, 
    engine_size_convertor,
    insurance_power_convertor)
import sys
sys.path.append('.')


def try_click(driver, button: str):
    try:
        driver.find_element(By.ID, button).click()
    except Exception:
        try:
            driver.find_element(By.XPATH, '//*[@id="popup-container"]/a').click()
            driver.find_element(By.ID, button).click()
        except Exception:
            pass


def get_insurance_price(car_data: dict):
    json_data = json.dumps(car_data, indent=2, ensure_ascii=False, separators=('', ' - '))
    # try to find the prices locally
    cwd = os.getcwd()
    with open(cwd+"/insurance.txt", "rb") as file:
        try:
            prices = pickle.load(file)
            return prices[json_data]
        except EOFError:
            prices = {}
        except KeyError:
            prices = prices # type: ignore
    # scrape the prices from the website
    driver = start_driver()
    wait_for_a_second(1)
    try:
        driver.find_element(By.ID, "thinkconsent-button-accept-all").click()
    except Exception:
        pass
    try:
        engine_size = engine_size_convertor(car_data["engine_size"])
        power = insurance_power_convertor(car_data["power"])

        # first page selectors
        Select(driver.find_element(By.ID, 'typeSelect')).select_by_value('1')
        Select(driver.find_element(By.ID, 'dvigatelSelect')).select_by_value(engine_size)
        Select(driver.find_element(By.ID, 'dvigatelType')).select_by_value(f'{car_data["fuel_type"]}')
        Select(driver.find_element(By.ID, 'ksiliSelect')).select_by_value(power)
        Select(driver.find_element(By.ID, 'seatNumberSelect')).select_by_value('5')
        Select(driver.find_element(By.ID, 'firstRegistrationYear')).select_by_value(f'{car_data["year"]}')
        Select(driver.find_element(By.ID, 'usefor')).select_by_value('1')
        if not car_data['registration']:
            driver.find_element(By.ID, 'noRegistration').send_keys('0')
        Select(driver.find_element(By.ID, 'reg_no')).select_by_value('CA')

        wait_for_a_second(1)    
        try_click(driver, 'continue')

        wait_for_a_second(1)
        # second page selectors
        # optional - age of the owner and driving experience by driving license
        if car_data['driver age']:
            driver.find_element(By.ID, 'vehicleOwnerAge').send_keys(car_data['driver age'])
        if car_data['driving experience']:
            Select(driver.find_element(By.ID, 'driverExperience')).select_by_value(car_data['driving experience'])
        else:
            Select(driver.find_element(By.ID, 'driverExperience')).select_by_value('5')
        Select(driver.find_element(By.ID, 'where_go')).select_by_value('druga')
        
        try_click(driver, 'calculate')
        wait_for_a_second()

        temp_prices = [
            price_convertor(el.text.split('\n')[1])
                for el in driver.find_elements(By.CLASS_NAME, "oi-compare-row")
            ]
    except Exception:
        return '0'

    prices[json_data] = [min(temp_prices), max(temp_prices)]
    with open(cwd+"/insurance.txt", "wb") as file:
        pickle.dump(prices, file)

    return prices[json_data]

def start_driver():
    driver = webdriver.Chrome()
    # the url of the insurance company
    url = "https://www.sdi.bg/onlineinsurance/showQuestionnaire.php"
    driver.get(url)
    return driver
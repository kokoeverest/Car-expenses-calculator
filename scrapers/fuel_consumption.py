from datetime import datetime
import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from conversions import wait_for_a_second


def find_fuel_consumption(brand: str, 
                          model: str, 
                          year_from: str, 
                          year_to: str, 
                          fuel_type: str, 
                          power_from: str, 
                          power_to: str,
                          avg_consumption = None 
    ):
    wait_for_a_second(1)
    
    Select(driver.find_element(By.ID, "manuf")).select_by_visible_text(brand.capitalize())
    wait_for_a_second(1)
    try:
        Select(driver.find_element(By.ID, "model")).select_by_visible_text(model.capitalize())
        Select(driver.find_element(By.ID, "fueltype")).select_by_visible_text(fuel_type.capitalize())
        driver.find_element(By.ID, "constyear_s").send_keys(year_from)
        driver.find_element(By.ID, "constyear_e").send_keys(year_to)
        driver.find_element(By.ID, "power_s").send_keys(int(power_from))
        driver.find_element(By.ID, "power_e").send_keys(int(power_to))
        driver.find_element(By.XPATH, "//*[@id='add']").submit()
        wait_for_a_second(4)

        avg_consumption = driver.find_element(By.CLASS_NAME, "consumption").text
        
        # build the nested dictionary to save the avg_consumption
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
        
        cwd = os.getcwd()
        with open(cwd+"/fuel_consumption.txt", "wb") as file:
            pickle.dump(all_cars_dict, file)
            
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


car_data = {
    'manuf': 'mazda', # car brand // Select
    'model': 'cx-5', # car model // Select
    'constyear_s': "2015", # car year from // <input type="text" name="constyear_s" id="constyear_s" value="" size="4">
    'constyear_e': "2015", # car year to // <input type="text" name="constyear_e" id="constyear_e" value="" size="4">
    'fueltype': 'gasoline', # car fuel type // Select
    'power_s': '140', # car engine power // <input type="text" name="power_s" id="power_s" value="" size="4">
    'power_e': '140' # car engine power // <input type="text" name="power_s" id="power_s" value="" size="4">
}

start = datetime.now()
print("Start: ", start)

# try to find the fuel consumption locally
with open(os.getcwd()+"/fuel_consumption.txt", "rb") as file:
    try:
        all_cars_dict = pickle.load(file)
    except EOFError:
        all_cars_dict = {}

if all(car_data.values()):
    brand, model, year_from, year_to, fuel_type, power_from, power_to = [el.capitalize() for el in car_data.values()]
    
    try:
        avg_consumption = all_cars_dict[brand][model][fuel_type][year_to][power_to]
    except KeyError:
        avg_consumption = None

    # if such record does not exist, start the driver and scrape it from the website
    if not avg_consumption:
        driver = start_driver()
        avg_consumption = find_fuel_consumption(brand, model, year_from, year_to, fuel_type, power_from, power_to)
else:
    avg_consumption = None

end = datetime.now()
diff = (end - start)
print(f"Duration: {diff}")
print("Average fuel consumption:", avg_consumption)

from data.db_connect import insert_query
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from models.car import Car
from common.exceptions import FuelConsumptionError
from services.scrapers.conversions import (
    wait_for_a_second,
    price_converter,
    find_correct_name,
    fuel_string_converter,
)
import sys

sys.path.append(".")


def find_fuel_consumption(
    brand: str, model: str, year: str, fuel_type: str, power: str, avg_consumption="0"
):
    # wait_for_a_second(1)
    with start_driver() as driver:
        brand = find_correct_name(
            brand,
            {opt.text for opt in Select(driver.find_element(By.ID, "manuf")).options},
        )
        if brand != "":
            Select(driver.find_element(By.ID, "manuf")).select_by_visible_text(brand)
        wait_for_a_second(1)
        try:
            model = find_correct_name(
                model,
                {
                    opt.text
                    for opt in Select(driver.find_element(By.ID, "model")).options
                },
            )
            if model != "":
                Select(driver.find_element(By.ID, "model")).select_by_visible_text(
                    model
                )
            Select(driver.find_element(By.ID, "fueltype")).select_by_visible_text(
                fuel_string_converter(fuel_type)
            )
            driver.find_element(By.ID, "constyear_s").send_keys(year)
            driver.find_element(By.ID, "constyear_e").send_keys(year)
            driver.find_element(By.ID, "power_s").send_keys(int(power) - 10)
            driver.find_element(By.ID, "power_e").send_keys(int(power) + 10)
            driver.find_element(By.XPATH, "//*[@id='add']").submit()
            wait_for_a_second()
            avg_consumption = driver.find_element(By.CLASS_NAME, "consumption").text
        except Exception as e:
            print(e)

    return avg_consumption


def start_driver():
    driver = webdriver.Chrome()
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


def get_fuel_consumption(car: Car):
    # if such record does not exist, start the driver and scrape it from the website
    if car.engine is not None:
        avg_consumption = find_fuel_consumption(
            car.brand,
            car.model,
            car.year,
            car.engine.fuel_type,
            car.engine.power_hp,
        )
        if avg_consumption != "0":
            # insert into the database, don't forget to update the cars_engines table!
            car.engine.consumption = price_converter(avg_consumption)
            car.engine.id = insert_query(
                """INSERT INTO `Car Expenses`.`Engines`
            (`Capacity`,`Power_hp`,`Power_kw`,`Fuel type`,`Emmissions category`,`Consumption`)
            VALUES(?, ?, ?, ?, ?, ?);""",
                (
                    car.engine.capacity,
                    car.engine.power_hp,
                    car.engine.power_kw,
                    car.engine.fuel_type,
                    car.engine.emissions_category,
                    car.engine.consumption,
                ),
            )
        if not car.engine.id:
            raise FuelConsumptionError("Fuel consumption not found!")

        _ = insert_query(
            "CALL `Car Expenses`.`update_cars_engines`(?, ?);", (car.id, car.engine.id)
        )

    return price_converter(avg_consumption)

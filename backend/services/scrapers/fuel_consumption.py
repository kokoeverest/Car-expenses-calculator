from data.db_connect import insert_query
from common.helpers import start_driver
from common.WEBSITES import FUEL_CONSUMPTION_WEBSITE
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from models.car import Car
from common.exceptions import FuelConsumptionError
from services.scrapers.conversions import (
    wait_for_a_second,
    string_to_float_converter,
    find_correct_name,
    fuel_string_converter,
)
import sys

sys.path.append(".")

def scrape_fuel_consumption(car: Car, avg_consumption="0"):
    with start_driver(FUEL_CONSUMPTION_WEBSITE) as driver:
        brand = find_correct_name(
            car.brand,
            {opt.text for opt in Select(driver.find_element(By.ID, "manuf")).options},
        )
        if brand != "":
            Select(driver.find_element(By.ID, "manuf")).select_by_visible_text(brand)
        wait_for_a_second(1)
        try:
            model = find_correct_name(
                car.model,
                {
                    opt.text
                    for opt in Select(driver.find_element(By.ID, "model")).options
                },
            )
            if model != "":
                Select(driver.find_element(By.ID, "model")).select_by_visible_text(
                    model
                )
            if car.engine and car.engine.fuel:
                Select(driver.find_element(By.ID, "fueltype")).select_by_visible_text(
                    fuel_string_converter(car.engine.fuel.fuel_type)
                )
            driver.find_element(By.ID, "constyear_s").send_keys(car.year)
            driver.find_element(By.ID, "constyear_e").send_keys(car.year)
            driver.find_element(By.ID, "power_s").send_keys(
                int(car.engine.power_hp) - 10 # type: ignore
            )
            driver.find_element(By.ID, "power_e").send_keys(
                int(car.engine.power_hp) + 10 # type: ignore
            )
            driver.find_element(By.XPATH, "//*[@id='add']").submit()
            wait_for_a_second()

            avg_consumption = driver.find_element(By.CLASS_NAME, "consumption").text
        except Exception as e:
            print(e)
        finally:
            return string_to_float_converter(avg_consumption)


def get_fuel_consumption(car: Car):
    """
    Get the current car's fuel consumption.
    """
    # if such record does not exist, start the driver and scrape it from the website
    if car.engine is not None:
        car.engine.consumption = scrape_fuel_consumption(car)
        if car.engine.consumption != float(0):
            # insert into the database, don't forget to update the cars_engines table!
            # good to be modified to have the two insert queries in one transaction

            car.engine.id = insert_query(
                """INSERT INTO `Car Expenses`.`Engines`
            (`Capacity`,`Power_hp`,`Power_kw`,`Fuel type`,`Emmissions category`,`Consumption`)
            VALUES(?, ?, ?, ?, ?, ?);""",
                (
                    car.engine.capacity,
                    car.engine.power_hp,
                    car.engine.power_kw,
                    car.engine.fuel.fuel_type,
                    car.engine.emissions_category,
                    car.engine.consumption,
                ),
            )
        if not car.engine.id:
            raise FuelConsumptionError("Fuel consumption not found!")

        _ = insert_query(
            "CALL `Car Expenses`.`update_cars_engines`(?, ?);", (car.id, car.engine.id)
        )

    return car.engine.consumption if car.engine else 0

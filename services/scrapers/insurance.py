from models.car import Car
from models.insurance import Insurance, INSURANCE_FUEL_VALUES as fuel
from data.db_connect import read_query, insert_query
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from services.scrapers.conversions import (
    wait_for_a_second,
    price_converter,
    engine_size_converter,
    insurance_power_converter,
)
import sys

sys.path.append(".")


def try_click(driver: WebDriver, button: str):
    try:
        driver.find_element(By.ID, button).click()
    except Exception:
        try:
            driver.find_element(By.XPATH, '//*[@id="popup-container"]/a').click()
            driver.find_element(By.ID, button).click()
        except Exception:
            pass


# not debugged!
def get_insurance_price(car: Car, registration, driver_age, driver_experience="5"):
    if car and car.engine and car.tax:
        car_data = (
            car.year,
            car.engine.capacity,
            car.engine.fuel_type,
            car.engine.power_hp,
            get_prefix(car.tax.city),
            registration,
            driver_age if driver_age is not None else "NULL",
            driver_experience,
        )
        data = next(
            iter(
                read_query(
                    """CALL `Car Expenses`.`get_insurance`(?,?,?,?,?,?,?,?);""",
                    car_data,
                )
            ),
            None,
        )
        if data:
            insurance = Insurance.from_query(*data)
            return insurance
        insurance = Insurance.from_list(*car_data)
        # scrape the prices from the website
        with start_driver() as driver:
            wait_for_a_second(1)
            try:
                driver.find_element(By.ID, "thinkconsent-button-accept-all").click()
            except Exception:
                pass
            try:
                engine_size = engine_size_converter(car.engine.capacity)
                power = insurance_power_converter(car.engine.power_hp)
                municipality = car_data[4]
                # first page selectors
                Select(driver.find_element(By.ID, "typeSelect")).select_by_value("1")
                Select(driver.find_element(By.ID, "dvigatelSelect")).select_by_value(
                    engine_size
                )
                Select(driver.find_element(By.ID, "dvigatelType")).select_by_value(
                    fuel[car.engine.fuel_type]
                )
                Select(driver.find_element(By.ID, "ksiliSelect")).select_by_value(power)
                Select(driver.find_element(By.ID, "seatNumberSelect")).select_by_value(
                    str(car.seats)
                )
                Select(
                    driver.find_element(By.ID, "firstRegistrationYear")
                ).select_by_value(car.year)
                Select(driver.find_element(By.ID, "usefor")).select_by_value("1")
                if not registration:
                    driver.find_element(By.ID, "noRegistration").send_keys("0")
                Select(driver.find_element(By.ID, "reg_no")).select_by_value(
                    municipality
                )

                wait_for_a_second(1)
                try_click(driver, "continue")

                wait_for_a_second(1)
                # second page selectors
                # optional - age of the owner
                if driver_age:
                    driver.find_element(By.ID, "vehicleOwnerAge").send_keys(driver_age)

                Select(driver.find_element(By.ID, "driverExperience")).select_by_value(
                    driver_experience
                )

                Select(driver.find_element(By.ID, "where_go")).select_by_value("druga")

                try_click(driver, "calculate")
                wait_for_a_second()

                temp_prices = [
                    price_converter(el.text.split("\n")[1])
                    for el in driver.find_elements(By.CLASS_NAME, "oi-compare-row")
                ]
                insurance.min_price, insurance.max_price = (
                    min(temp_prices),
                    max(temp_prices),
                )
                _ = insert_query(
                    f"""CALL `Car Expenses`.`add_insurance`(
                        '{car.year}', '{car.engine.capacity}', '{car.engine.fuel_type}', 
                        '{car.engine.power_hp}', '{municipality}', {registration}, 
                        {driver_age if driver_age is not None else "NULL"}, '{driver_experience}', 
                        {insurance.min_price}, {insurance.max_price}, '{date.today()}');"""
                )

            except Exception as e:
                print(str(e))
                insurance.min_price, insurance.max_price = 0, 0

    return insurance


def start_driver():
    driver = webdriver.Chrome()
    # the url of the insurance company
    url = "https://www.sdi.bg/onlineinsurance/showQuestionnaire.php"
    driver.get(url)
    return driver


def get_prefix(city_name: str):
    prefix: tuple[str] | str = next(
        iter(
            read_query(
                f"CALL `Car Expenses`.`get_municipality_prefix`('%{city_name}%');"
            )
        ),
        "",
    )

    if prefix:
        return prefix[0]

    raise ValueError("Registration plate prefix not found!")

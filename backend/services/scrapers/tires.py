from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
from datetime import date
import re
import sys
from models.car import Car
from common.helpers import start_driver, collection_to_dict
from common.WEBSITES import TIRES_WEBSITE

sys.path.append(".")
from models.tire import Tire
from services.scrapers.conversions import wait_for_a_second
from data.db_connect import (
    read_query,
    update_query,
    multiple_insert_queries,
)

"""This scraper should accept the car object and add the tires sizes and prices to the calculations"""

FIND_TIRE_SIZE_PATTERN = r"\d{3}/\d{2}R\d{2}|\d{3}/\d{2}ZR\d{2}"
FIND_TIRE_PRICES_PATTERN = r"^\d+,\d+|^\d+\.\d+|^\d+"


def find_tire_sizes(driver: webdriver.Chrome):
    """Search for the available car tires using the regular expression pattern"""
    possible_tire_sizes = set()
    wait_for_a_second()
    table_rows = driver.find_elements(By.TAG_NAME, "tr")

    for row in table_rows[1:]:
        matches = re.findall(FIND_TIRE_SIZE_PATTERN, row.text)
        if len(matches) > 0:
            possible_tire_sizes.add(*matches)

    return possible_tire_sizes


def collect_tires_prices(
    tire_sizes: set | list, driver: webdriver.Chrome
) -> list[Tire] | list:
    """Search for the minimum and maximum price of each tire in the list.
    Returns a new list with Tire objects"""
    tires = []
    for size in tire_sizes:
        w, h, i = size[:3], size[4:6], size[-2:]

        prefix = "ZR" if size[6:8] == "ZR" else "R"
        print(f"Collecting prices for {w}/{h}/{i} with prefix {prefix} ({size})")
        link_url = f"eshop/search?type=1&width={w}&height={h}&inch={i}"

        wait_for_a_second()
        # tires are sorted by lowest price by default
        driver.get(TIRES_WEBSITE + link_url)
        tire = Tire(width=w, height=h, size=i, prefix=prefix)
        tire.min_price = add_product_price(driver)

        wait_for_a_second()
        # sort tires by highest price first
        Select(driver.find_element(By.ID, "sortby")).select_by_value("2")
        tire.max_price = add_product_price(driver)
        tires.append(tire)
    return tires


def add_product_price(driver: webdriver.Chrome) -> float:
    """Get the price of the first found product"""
    wait_for_a_second(1)

    try:
        product = driver.find_element(By.CLASS_NAME, "price").text

        matches = re.findall(FIND_TIRE_PRICES_PATTERN, product)
        if len(matches) > 0:
            product: str = matches[0]

            # if the price of one tire is ridiculously high, above 1000 leva, it will be separated by a comma
            product = product.replace(",", "")
        return float(product)
    except Exception:
        return float(0)


def get_tires_prices(car: Car):
    """The main logic of this scraper -> look for the tires sizes and prices in the database and if some
    of the info is missing, scrape it from the website and update the database"""
    possible_sizes = re.findall(FIND_TIRE_SIZE_PATTERN, car.tires)  # type: ignore
    print("Before scraping: ", possible_sizes)

    # if there are no posiible tires sizes recorded in the db, try to scrape them
    if possible_sizes == []:
        possible_sizes = scrape_possible_tires(car.brand, car.model, car.year)
        if possible_sizes == []:
            return possible_sizes
        update_query(
            f"""
            CALL `Car Expenses`.`update_car_tires`('{car.brand}', '{car.model}', {car.year}, "{possible_sizes}");"""
        )

    # then look for the price of each tire and see if there are missing records in the database
    existing_tires = return_list_with_tire_objects(possible_sizes)
    print("Existing tires: ", existing_tires)
    missing_sizes = set(possible_sizes).difference(
        set(str(tire) for tire in existing_tires)
    )
    print("Missing sizes: ", missing_sizes)
    if len(missing_sizes) == 0:
        return sorted(existing_tires, key=lambda x: x.size)

    # if there are missing tires in the ddatabase - scrape them and update the info for each tire
    today = date.today()
    collected_tires = []
    missing_query = []

    with start_driver(TIRES_WEBSITE) as driver:
        collected_tires = collect_tires_prices(missing_sizes, driver)

    for tire in collected_tires:
        missing_query.append(
            f"""call `Car Expenses`.add_tire('{tire.prefix}', '{tire.width}', '{tire.height}', '{tire.size}',\
                {tire.min_price}, {tire.max_price}, '{today}');"""
        )

    _ = multiple_insert_queries(missing_query)

    return sorted(list(set(collected_tires + existing_tires)), key=lambda x: x.size)


def scrape_possible_tires(brand, model, year):
    """Start the webdriver and search for the possible tire sizes for that car model"""

    print(f"Scraping tires prices for {brand} {model} {year}")

    with start_driver(TIRES_WEBSITE) as driver:
        Select(driver.find_element(By.ID, "makers")).select_by_value(brand)
        wait_for_a_second()
        Select(driver.find_element(By.ID, "models")).select_by_value(model)
        wait_for_a_second()
        Select(driver.find_element(By.ID, "years")).select_by_value(year)
        wait_for_a_second()
        button = driver.find_element(By.ID, "get_wheelsize")
        wait_for_a_second(1)
        button.click()

        possible_sizes = find_tire_sizes(driver)

    return list(sorted(possible_sizes))


def return_list_with_tire_objects(possible_sizes_list: list):
    """Retrieve info from the database for each tire in the list and convert it in a Tire object"""

    read_query_result = "SELECT `Width`, `Height`, `Prefix`, `Radius`, `Min price`, `Max price` FROM Tires WHERE "

    for tire_size in possible_sizes_list:
        w, h, i = tire_size[:3], tire_size[4:6], tire_size[-2:]
        read_query_result += (
            f" (`Width` = '{w}' AND `Height` = '{h}' AND `Radius` = '{i}') OR"
        )
    result = read_query(read_query_result.removesuffix(" OR"))

    return  [Tire(**collection_to_dict(el, Tire)) for el in result] # type: ignore

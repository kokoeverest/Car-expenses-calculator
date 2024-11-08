from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from . import WEBSITES


def headless_options():
    headless_options = webdriver.ChromeOptions()
    headless_options.add_argument("--headless=new")
    headless_options.add_argument("--disable-logging")
    return headless_options


def options():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-logging")
    return options


def start_driver(url, headless=False):
    """
    Start an instance of Chrome webdriver with the headless option off by default.
    """
    driver = (
        webdriver.Chrome(headless_options())
        if headless
        else webdriver.Chrome(options=options())
    )
    driver.get(url)

    return close_cookies_window(driver, url)


def close_cookies_window(driver: webdriver.Chrome, url):
    """
    Deal with the cookies pop up windows across the websites.
    """
    if url == WEBSITES.FUEL_CONSUMPTION_WEBSITE:
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

    elif url == WEBSITES.VIGNETTE_WEBSITE:
        try:
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                if button.text == "Разбрах":
                    button.click()
                    break
            else:
                raise Exception("Consent button was not found")
        except Exception as e:
            print(str(e))
            pass

    return driver


def collection_to_dict(collection: list | tuple, entity: BaseModel):
    """
    Return an instance of app models, using the Pydantic BaseModel initializer. Made for simplicity and code reusability
    (trying to eliminate the from_query() classmethod with all the variable assignments).

    Args:
        collection (list | tuple): the collection containing the values which will map to the BaseModel.model_fields

        entity (BaseModel): its model_fields will be used as keys to be mapped to the collection values.
    """
    return {k: collection[i] for i, k in enumerate(entity.model_fields)}

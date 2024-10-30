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


def close_cookies_window(driver, url):
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

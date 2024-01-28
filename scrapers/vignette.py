from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import os
import re
import sys
sys.path.append('.')


def start_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)

    # deal with the cookies pop up window
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

def get_vignette_price(url='https://vinetki.bg/prices'):
    driver = start_driver(url)
    soup = bs(driver.page_source, features="lxml").find_all('td', string=re.compile('ГОДИШНА'))
    price = list(soup[0].next_elements)[4].rstrip(' лв.').replace(',', '.')
    return float(price)

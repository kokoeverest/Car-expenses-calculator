from bs4 import BeautifulSoup as bs
from common.WEBSITES import VIGNETTE_WEBSITE
# from common.helpers import start_driver
import requests
import re
import sys

sys.path.append(".")



def get_vignette_price(url=VIGNETTE_WEBSITE):
    """start_driver needed if the request.get(url) fails for some reason (cookies window for example)?"""
    print("Scraping vignette price...")
    try:
        response = requests.get(url)
        soup = bs(response.text, features="lxml")
        soup = soup.find_all("td", string=re.compile("ГОДИШНА"))
        price = list(soup[0].next_elements)[4].rstrip(" лв.").replace(",", ".")
    except Exception:
        # uncomment and implement if needed
        # with start_driver(VIGNETTE_WEBSITE) as driver:
        #     raise NotImplementedError("Vignette service not implemented")
        price = 0
    return float(price)

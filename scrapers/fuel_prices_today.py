import requests
from bs4 import BeautifulSoup as bs
import sys
sys.path.append('.')


def get_fuel_prices(url='https://m.fuelo.net/m/prices'):
    
    fuels_dict = {
        'Бензин A95': 'gasoline',
        'Дизел': 'diesel',
        'Пропан Бутан': 'lpg',
        'Метан': 'cng',
        'Дизел премиум': 'premium',
        'Бензин A98': 'gasoline A98',
        'Бензин A100': 'gasoline A100'
    }

    result = requests.get(url)
    soup = bs(result.text).find_all('h4')

    prices = {}
    for el in soup:
        raw = el.text.split(' ')

        if len(raw) == 3: 
            fuel_type, price = str(raw[0] + ' ' + raw[1]), raw[2]
        elif len(raw) == 2:
            fuel_type, price = raw 
        else:
            continue

        if 'цени от' not in price:
            new_str = fuels_dict.get(fuel_type)
            fuel_type = fuel_type.replace(f'{fuel_type}', f'{new_str}')
            prices[fuel_type] = float(price.replace(',', '.').rstrip('лв.'))

    return prices
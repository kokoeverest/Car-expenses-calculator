from datetime import datetime
import time
import re
from fuzzywuzzy import fuzz

def word_versions(word: str):
    copy_of_word = word
    if not word.isalpha() and not word.isdigit() and not word[0].isdigit():
        word_as_list = list(word)
        for i in range(len(word_as_list)):
            if word_as_list[i].isdigit() and i > 0:
                word_as_list.insert(i, " ")
                break
        word = "".join(word_as_list)
    return {
        copy_of_word,
        word.lower(), 
        word.upper(), 
        word.capitalize(), 
        word.replace("-", ""), 
        word.replace(" ", '.'), 
        word.replace("-", " "),
        word.replace("-", "."), 
        word.replace(" ", "-").lower(),
        word.replace(" ", "-").upper(), 
        word.replace("-", "").capitalize(),
        word.replace(" ", "-").capitalize(), 
        word.replace(" ", ".").capitalize(),
        word.replace("-", ".").capitalize(), 
        "".join(w for w in word.split()), 
        " ".join(w.capitalize() for w in word.split()), 
        "-".join(w.capitalize() for w in word.split()),
        ".".join(w.capitalize() for w in word.split()),
        "".join(w.capitalize() for w in word.split())
    }

def find_correct_name(search: str, options: set) -> str:
    versions = word_versions(search)
    try:
        result = next(iter(options.intersection(versions)), "")
        if not result:
            raise
    except:
        result = next(iter([
                    word for word in options 
                    for option in versions 
                    if option in word 
                    and fuzz.ratio(option, word) > 90]), "")
    return result


def wait_for_a_second(seconds=2):
    '''Wait a second, don't put too much pressure on the server :-)'''
    return time.sleep(seconds)

def age_convertor(age) -> str:
    if len(age) == 4:
        age = calculate_age(age)
    else:
        age = int(age)
    result = 0
    
    if 6 <= age <= 10:
        result += 1
    elif 11 <= age <= 15:
        result += 2
    elif 15 <= age <= 20:
        result += 3
    elif age > 20:
        result += 4
    
    return str(result)

def calculate_age(year) -> int:
    current_year = datetime.now().year
    return current_year - int(year)

def get_euro_category_from_car_year(year: str):
    if year == "EEV":                return year
    if int(year) < 1992:             return "без екологична категория"
    elif 1992 <= int(year) < 1996:   return "Euro 1"
    elif 1996 <= int(year) < 2000:   return "Euro 2"
    elif 2000 <= int(year) < 2005:   return "Euro 3"
    elif 2005 <= int(year) < 2009:   return "Euro 4"
    elif 2009 <= int(year) < 2015:   return "Euro 5"
    else:                            return "Euro 6"

def calculate_euro_category(string: str):
    if string == "EEV":        return "7"
    if string.isalpha():       return "0"
    else:                      return string[-1]
    
def hp_to_kw_converter(hp: int):
    return str(int(hp) * 0.746)

def kw_to_hp_convertor(kw: int):
    pass

def convert_car_string(string: str):
    return string.replace(" ", "-").lower()

def price_convertor(product: str):
    try:
        return float(product.replace(',', '.'))
    except:
        return float(0)    

def engine_size_convertor(size: str) -> str:
    if int(size) <= 800:             return '800'
    elif 2600 < int(size) <= 3000:   return '3000'
    elif 3000 < int(size) <= 3200:   return '3200'
    elif 3200 < int(size) <= 3500:   return '3500'
    else:                            return '3501'

def insurance_power_convertor(power: str) -> str:
    if int(power) <= 90:            return '66'
    elif 90 < int(power) <= 101:    return '74'
    elif int(power) == 102:         return '75'
    elif 102 < int(power) <= 120:   return '88'
    elif 120 < int(power) <= 150:   return '110'
    elif 150 < int(power) <= 160:   return '118'
    elif 160 < int(power) <= 170:   return '125'
    else:                           return '126'


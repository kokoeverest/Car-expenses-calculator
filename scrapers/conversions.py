from datetime import datetime
import time

def wait_for_a_second(sec: int):
    '''Wait a sec, don't put too much pressure on the server :-)'''
    return time.sleep(sec)

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

    if not isinstance(year, int):
        year = int(year)

    return current_year - year


def calculate_euro_category(string: str):
    if string == "EEV":
        return "7"
    if string.isalpha():
        return "0"
    else:
        return string[-1]
    

def hp_to_kw_converter(hp: int):
    return str(int(hp) * 0.746)

def convert_car_string(string: str):
    return string.replace(" ", "-").lower()

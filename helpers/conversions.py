from datetime import datetime


def age_convertor(age: str):
    if len(age) == 4:
        age = calculate_age(age)
    else:
        age = int(age)
    result = ""
    if 0 == age <= 5:
        result = "0"
    elif 6 <= age <= 10:
        result = "1"
    elif 11 <= age <= 15:
        result = "2"
    elif 15 <= age <= 20:
        result = "3"
    elif age > 20:
        result = "4"
    return result


def calculate_age(year):
    current_year = datetime.now().year

    if not isinstance(year, int):
        year = int(year)

    return current_year - year


def calculate_eoro_catagory(string: str):
    if string == "EEV":
        return 7
    if string.isalpha():
        return 0
    else:
        return int(string[-1])
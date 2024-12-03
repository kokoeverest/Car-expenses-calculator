from datetime import datetime
import time
from fuzzywuzzy import fuzz


def wait_for_a_second(seconds=2):
    """Wait a second, don't put too much pressure on the server :-)"""
    return time.sleep(seconds)


def find_correct_name(search: str, options: set[str]) -> str:
    versions = word_versions(search)
    try:
        result = next(iter(options.intersection(versions)), "")
        if not result:
            raise
    except Exception:
        result = next(
            iter(
                [
                    word
                    for word in options
                    for option in versions
                    if option in word and fuzz.ratio(option, word) > 90
                ]
            ),
            "",
        )
    return result


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
        copy_of_word.lower(),
        copy_of_word.upper(),
        word.lower(),
        word.upper(),
        word.capitalize(),
        word.replace(" ", ""),
        word.replace("-", ""),
        word.replace(" ", "."),
        word.replace("-", " "),
        word.replace("-", "."),
        word.replace(" ", "-").lower(),
        word.replace(" ", "-").upper(),
        word.replace("-", "").capitalize(),
        word.replace(" ", "-").capitalize(),
        word.replace(" ", ".").capitalize(),
        word.replace("-", ".").capitalize(),
        "".join(w for w in word.split()),
        " ".join(w.capitalize() for w in word.split("-")),
        " ".join(w.capitalize() for w in word.split()),
        "-".join(w.capitalize() for w in word.split()),
        ".".join(w.capitalize() for w in word.split()),
        "".join(w.capitalize() for w in word.split()),
    }


def tax_age_converter(age: str | int) -> str:
    if isinstance(age, str) and len(age) == 4:
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


def calculate_age(year: str) -> int:
    current_year = datetime.now().year
    return current_year - int(year)


def tax_get_euro_category_from_car_year(year: str):
    if year == "EEV":
        return year
    if int(year) < 1992:
        return "без екологична категория"
    elif 1992 <= int(year) < 1996:
        return "Euro 1"
    elif 1996 <= int(year) < 2000:
        return "Euro 2"
    elif 2000 <= int(year) < 2005:
        return "Euro 3"
    elif 2005 <= int(year) < 2009:
        return "Euro 4"
    elif 2009 <= int(year) < 2015:
        return "Euro 5"
    else:
        return "Euro 6"


def calculate_euro_category(string: str):
    if string == "EEV":
        return "7"
    if string.isalpha():
        return "0"
    else:
        return string[-1]


def hp_to_kw_converter(hp: str):
    return str(round(int(hp) * 0.746))


def validate_engine_capacity(string: str):
    if string.isdigit() and len(string) > 2:
        return string
    
    string = string.replace(",", "") if "," in string else string.replace(".", "")

    if len(string) == 2:
        string = str(int(string) * 100)

    if len(string) == 3:
        string += "0"

    return validate_engine_capacity(string)


def kw_to_hp_converter(kw: str):
    return str(round(int(kw) * 1.34102209))


def car_string_converter(string: str):
    return string.replace(" ", "-").lower()


def string_to_float_converter(price: str):
    try:
        return float(price.replace(",", "."))
    except Exception:
        return float(0)


def insurance_engine_size_converter(size: str) -> str:
    if int(size) <= 800:
        return "800"
    elif 800 < int(size) <= 2600:
        return size
    elif 2600 < int(size) <= 3000:
        return "3000"
    elif 3000 < int(size) <= 3200:
        return "3200"
    elif 3200 < int(size) <= 3500:
        return "3500"
    else:
        return "3501"


def insurance_power_converter(power: str) -> str:
    if int(power) <= 90:
        return "66"
    elif 90 < int(power) <= 101:
        return "74"
    elif int(power) == 102:
        return "75"
    elif 102 < int(power) <= 120:
        return "88"
    elif 120 < int(power) <= 150:
        return "110"
    elif 150 < int(power) <= 160:
        return "118"
    elif 160 < int(power) <= 170:
        return "125"
    else:
        return "126"


def done(string="Done"):
    print(string + "\n" + "-" * 33)


def fuel_string_converter(string: str):
    fuels = {
        "eev": "Electricity",
        "cng": "CNG",
        "lpg": "LPG",
        "hybrid gasoline": "Plug-in hybrid gasoline",
        "hybrid diesel": "Plug-in hybrid diesel",
    }

    try:
        return fuels[string.lower()]
    except KeyError:
        return string.capitalize()

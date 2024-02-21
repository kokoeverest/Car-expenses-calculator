from enum import Enum

class Insurance:
    
    def __init__(self, ) -> None:
        pass


class InsuranceFuelValues(Enum):
    gasoline = '1'
    diesel = '2'
    hybrid_gasoline = '3'
    hybrid_diesel = '4'
    gasoline_lpg_cng = '5'
    diesel_lpg_cng = '6'
    eev = '7'
    lpg_cng_only = '8'


class FuelsDictionary(Enum):
    gasoline = 'Бензин'
    diesel = 'Дизел'
    lpg = 'Пропан Бутан'
    cng = 'Метан'
    premium = 'Премиум'
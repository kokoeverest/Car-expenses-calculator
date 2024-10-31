class WrongCarData(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class FuelConsumptionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
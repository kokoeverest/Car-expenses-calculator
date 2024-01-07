class Tire:
    
    def __init__(self, width, height, size, min_price=None, max_price=None) -> None:
        self.width = width
        self.height = height
        self.size = size
        self.min_price = min_price
        self.max_price = max_price


    def __repr__(self) -> str:
        return f"{self.width}/{self.height}R{self.size}"
    

    def __eq__(self, other) -> bool:
        return f"{self.width}/{self.height}R{self.size}" == f"{other.width}/{other.height}R{other.size}"
             

    def get_prices_list(self):
        return [f"{self.min_price} лв", f"{self.max_price} лв"]
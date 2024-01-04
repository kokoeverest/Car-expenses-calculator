class Tire:
    
    def __init__(self, width, height, size, min_price=None, max_price=None) -> None:
        self.width = width
        self.height = height
        self.size = size
        self.min_price = min_price
        self.max_price = max_price


    def __repr__(self) -> str:
        return f"{self.width}/{self.height}R{self.size}"
    

    def get_prices_list(self):
        return [self.min_price, self.max_price]
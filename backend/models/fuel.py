from datetime import datetime
from pydantic import BaseModel

class Fuel(BaseModel):
    fuel_type: str
    price: float = 0
    date: datetime | None = None
from models.car import Car
from typing import Any
from models.engine import Engine
from models.fuel import Fuel
from models.insurance import Insurance
from models.tax import Tax
from models.tire import Tire

car_responses: dict[int | str, dict[str, Any]] | None = {
    200: {
        "description": "Successful",
        "content": {
            "application/json": {
                "example": Car(
                    id=0,
                    brand="string",
                    model="string",
                    year="2010",
                    engine=Engine(
                        id=0,
                        capacity="2000",
                        power_hp="131",
                        power_kw="100",
                        fuel=Fuel(fuel_type="gasoline"),
                        emissions_category="Euro 4",
                    ),
                    tax=Tax(
                        city="София",
                        municipality="Столична",
                        car_age=14,
                        euro_category="Euro 4",
                        car_power_kw="100",
                    ),
                    tires=[Tire(width="195", height="65", size="14")],
                    insurance=Insurance(
                        id=0,
                        year="2010",
                        engine_size="2000",
                        power="100",
                        fuel_type="gasoline",
                        municipality="Столична",
                    ),
                )
            }
        },
    },
    204: {
        "description": "No content",
        "content": {"application/json": {"example": "No car data!"}},
    },
    400: {
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": "Invalid engine capacity! (No whitespaces, please)"
            }
        },
    },
    404: {
        "description": "Not Found",
        "content": {"application/json": {"example": "Not found!"}},
    },
    500: {
        "description": "Internal Server Error",
        "content": {"application/json": {"example": "Oops, something went wrong...!"}},
    },
}

from typing import Annotated
from fastapi import APIRouter, Form
import services.car_services as cs
from routers.responses import car_responses
import sys

sys.path.append(".")

car_router = APIRouter(prefix="/api")


@car_router.get("/", tags=["Car price builder"], responses=car_responses)
# def get_car_prices(
#     brand: Annotated[str, Form()],
#     model: Annotated[str, Form()],
#     year: Annotated[str, Form()],
#     fuel_type: Annotated[str, Form()],
#     engine_capacity: Annotated[str, Form()],
#     city: Annotated[str, Form()],
#     power_hp: Annotated[str, Form()] = "",
#     power_kw: Annotated[str, Form()] = "",
#     car_price: Annotated[str, Form()] | None = None,
# ):
def get_car_prices(
    brand: str,
    model: str,
    year: str,
    fuel_type: str,
    engine_capacity: str,
    city: str,
    power_hp: str = "",
    power_kw: str = "",
    car_price: str | None = None,
):
    car = cs.build_car(brand, model, year, power_hp, power_kw, fuel_type, engine_capacity, city, car_price)

    return car

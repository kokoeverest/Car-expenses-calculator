from typing import Annotated
from common.exceptions import WrongCarData
from fastapi import APIRouter, Body, Response, status, Form
from models.car import Car
import services.car_services as cs
from routers.responses import car_responses
import sys

sys.path.append(".")

router = APIRouter(prefix="/car")
api_router = APIRouter(prefix="/api")
enums_router = APIRouter(prefix="/api/enums")


@api_router.post("/car", tags=["Car price API"], responses=car_responses)
def get_car_prices(
    brand: Annotated[str, Body()] = "Volvo",
    model: Annotated[str, Body()] = "XC60",
    year: Annotated[str, Body()] = "2010",
    fuel_type: Annotated[str, Body()] = "diesel",
    engine_capacity: Annotated[str, Body()] = "2.4",
    city: Annotated[str, Body()] = "София",
    power_hp: Annotated[str, Body()] = "",
    power_kw: Annotated[str, Body()] = "120",
    car_price: Annotated[str, Body()] = "",
):
    try:
        car: Car = cs.build_car(
            brand,
            model,
            year,
            power_hp,
            power_kw,
            fuel_type,
            engine_capacity,
            city,
            car_price,
        )
    except RecursionError:
        return Response(
            content="Invalid engine capacity! (No whitespaces, please)",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except WrongCarData:
        return Response(
            content=f"No information for {brand} {model}-{year} could be found",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        print(str(e))
        return Response(
            content="Something went wrong",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return car


@router.post("",tags=["Car price client form"], responses=car_responses)
def get_car_prices_from_form(
    brand: Annotated[str, Form()],
    model: Annotated[str, Form()],
    year: Annotated[str, Form()],
    fuel_type: Annotated[str, Form()],
    engine_capacity: Annotated[str, Form()],
    city: Annotated[str, Form()],
    power_hp: Annotated[str, Form()] = "",
    power_kw: Annotated[str, Form()] = "",
    car_price: Annotated[str, Form()] = "",
):
    print("Retrieving data from form: ")
    return get_car_prices(
        brand,
        model,
        year,
        fuel_type,
        engine_capacity,
        city,
        power_hp,
        power_kw,
        car_price,
    )


@enums_router.get("/{brand}/{model}/years")
async def get_years_by_brand_and_model(brand: str, model: str):
    years = await cs.get_years_by_car_model(brand, model)

    return years


@enums_router.get("/{brand}/models")
async def get_models_by_brand(brand: str):
    models = await cs.get_models_by_car_brand(brand)

    return models


@enums_router.get("/brands")
async def get_all_car_brands():
    brands = await cs.get_car_brands()

    return brands


@enums_router.get("/cities")
async def get_city_names():
    cities = await cs.get_cities()

    return cities

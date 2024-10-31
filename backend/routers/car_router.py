from typing import Annotated
from common.exceptions import WrongCarData
from fastapi import APIRouter, Response, status, Form
from fastapi.responses import JSONResponse
import services.car_services as cs
from routers.responses import car_responses
import sys

sys.path.append(".")

car_router = APIRouter()


@car_router.get("/api/", tags=["Car price API"], responses=car_responses)
def get_car_prices(
    brand: str = "Volvo",
    model: str = "XC60",
    year: str = "2010",
    fuel_type: str = "diesel",
    engine_capacity: str = "2.4",
    city: str = "София",
    power_hp: str = "",
    power_kw: str = "120",
    car_price: str | None = None,
):
    try:
        car = cs.build_car(
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
            status_code=status.HTTP_204_NO_CONTENT,
        )
    except Exception as e:
        print(str(e))
        return Response(
            content="Something went wrong",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return JSONResponse(car)


@car_router.get("/", tags=["Car price client form"], responses=car_responses)
def get_car_prices_from_form(
    brand: Annotated[str, Form()],
    model: Annotated[str, Form()],
    year: Annotated[str, Form()],
    fuel_type: Annotated[str, Form()],
    engine_capacity: Annotated[str, Form()],
    city: Annotated[str, Form()],
    power_hp: Annotated[str, Form()] = "",
    power_kw: Annotated[str, Form()] = "",
    car_price: Annotated[str, Form()] | None = None,
):
    pass
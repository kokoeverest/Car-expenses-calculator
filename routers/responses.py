from models.car import Car
from typing import Any

car_responses: dict[int | str, dict[str, Any]] | None = {
    200: {
        "description": "Successful",
        "content": {
            "application/json": {
                "example": Car(
                    brand="string", model="string", year="string", price="string"
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
        "content": {"application/json": {"example": "Invalid engine capacity! (No whitespaces, please)"}},
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

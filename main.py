from fastapi import FastAPI
from routers.car_router import car_router

app = FastAPI()
app.include_router(car_router)
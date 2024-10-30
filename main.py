import uvicorn
from fastapi import FastAPI
from routers.car_router import car_router

app = FastAPI()
app.include_router(car_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
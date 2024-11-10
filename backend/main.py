import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import car_router
from common.configurations import app_cors_origins as origins

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(car_router.router)
app.include_router(car_router.api_router)
app.include_router(car_router.enums_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

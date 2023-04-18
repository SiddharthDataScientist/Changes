from fastapi import  FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field



app = FastAPI()

class Car:
    Company: str
    Car: str
    Engine: str
    color: str
    Gear: int
    Rating: float

    def __init__(self,Company,Car,Engine,Color,Gear,Rating):
        self.Company = Company
        self.Car = Car
        self.Engine = Engine
        self.color = Color
        self.Gear = Gear
        self.Rating = Rating


class CarRequest(BaseModel):
    Company: str = Field(min_length=2)
    Car: str = Field(min_length=2)
    Engine: str = Field(min_length=2)
    color: str = Field(min_length=2)
    Gear: int
    Rating: float = Field(gt=0.0, lt=5.1)


    class Config:
        schema_extra = {
            'example' : {
            'Company': 'Tata',
            'Car': 'Punch',
            'Engine': 'Petrol',
            'color': 'White',
            'Gear' : 5,
            'Rating': 4.0
            }
        }



CARS = [
    Car('Tata', 'Nexon', 'Diesel', 'White', 6, 4.5),
    Car('Honda', 'City', 'Petrol', 'Grey', 5, 3.8),
    Car('Hyundai', 'i20', 'CNG', 'Red', 5, 4),
    Car('Mini Copper', 'Countryman', 'Diesel', 'White', 5, 5),
    Car('Audi', 'A8', 'Electric', 'Black', 5, 4.5),
        
]

@app.get("/cars")
async def read_all_cars():
    return CARS

@app.get("/cars/")
async def read_car_by_rating(car_rating: float):
    cars_to_return = []
    for car in CARS:
        if car.Rating == car_rating:
            cars_to_return.append(car)
    return cars_to_return


@app.post("/create-car")
async def create_car(car_request: CarRequest):
    new_car = Car(**car_request.dict())
    CARS.append(new_car)


@app.put("/cars/update_car")
async def update_car(car: CarRequest):
    for i in range(len(CARS)):
        if CARS[i].Company == car.Company:
            CARS[i] = car
            
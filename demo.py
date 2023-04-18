from fastapi import FastAPI, Body
import uvicorn
import psycopg2
from psycopg2.extras import RealDictCursor
import time 

app = FastAPI()

while True:

    try:
       conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Password@0987',cursor_factory = RealDictCursor)
       cursor = conn.cursor()
       print("Database connection was succesfull")
       break

    except Exception as error:
       print("Connecting database failed")
       print("Error: ", error)
       time.sleep(2)

CARS = [
    {'Company': 'TATA', 'Car': 'Altroz', 'Engine': 'Petrol', 'Geartype': 'Manual', 'Color': 'White', 'MaxSpeed':'160Km/h','No.': 'KA02H0321'},
    {'Company': 'Honda', 'car': 'City', 'Engine': 'Diesel', 'Geartype': 'Automatic', 'Color': 'Black', 'MaxSpeed':'200Km/h','No.': 'KA79HK7851'},
    {'Company': 'Hyundai', 'car': 'i20', 'Engine': 'CNG', 'Geartype': 'Automatic', 'Color': 'Blue', 'MaxSpeed':'180Km/h', 'No.': 'KA39F9721'},
    {'Company': 'Mini Copper', 'car': 'Countryman', 'Engine': 'Petrol', 'Geartype': 'Automatic', 'Color': 'Black', 'MaxSpeed':'225Km/h', 'No.': 'KA20MA6501'},
    {'Company': 'Audi', 'car': 'Q8', 'Engine': 'Diesel', 'Geartype': 'Automatic', 'Color': 'White', 'MaxSpeed':'220Km/h', 'No.': 'KA08H3751'}
]

@app.get("/cars")
async def read_all_cars():
    cursor.execute(""" SELECT * FROM Cars""")
    cars = cursor.fetchall
    print(cars)
    return CARS


@app.get("/cars/{car_title}")
async def read_company(car_comapny: str):
    for car in CARS:
        if car.get('Company').casefold() == car_comapny.casefold():
            return car

    
@app.get("/cars/")
async def read_color_by_query(color : str):
    car_to_return = []
    for car in CARS:
        if car.get('Color').casefold() == color.casefold():
            car_to_return.append(car)
    return car_to_return

        
@app.get("/cars/engine/")
async def read_engine_by_query(engine: str):
    car_to_be_returned = []
    for cars in CARS:
        if cars.get('Engine').casefold() == engine.casefold():
            car_to_be_returned.append(cars)
    return car_to_be_returned

@app.post("/cars/create_car")
async def create_car(new_car = Body()):
    CARS.append(new_car)


@app.put("/cars/upadte_car")
async def update_car(upadted_car = Body()):
    for i in range(len(CARS)):
        # Even if i mention casfold() why it shows error
        if CARS[i].get('Color').casefold() == upadted_car.get('Color').casefold():
            CARS[i] = upadted_car

@app.delete("/cars/delete_car{car_color}")
async def delete_car(car_color: str):
    for i in range(len(CARS)):
        if CARS[i].get('Color').casefold() == car_color.casefold():
            CARS.pop(i)
            break




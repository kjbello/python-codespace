from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated, Callable
import uvicorn
import logging

from services.cars_sql_data import CarsSqlData
from services.notification import get_notify
import models
import schemas

# # ensures all tables are created
# from database import engine
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

CarsSqlDataType = Annotated[CarsSqlData, Depends(CarsSqlData)]
NotifyType = Annotated[Callable[[str, str], str], Depends(get_notify)]


@app.get("/cars", response_model=list[schemas.Car])
async def all_cars(
    cars_sql_data: CarsSqlDataType,
) -> list[models.Car]:
    try:
        return cars_sql_data.get_cars()
    except Exception as exc:
        logging.error("database call failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/cars/{car_id}", response_model=schemas.Car)
async def one_car(
    car_id: int,
    cars_sql_data: CarsSqlDataType,
) -> models.Car:
    if car_id < 1:
        raise HTTPException(status_code=400, detail="Invalid car id")

    try:
        car_model = cars_sql_data.get_car(car_id)
    except Exception as exc:
        logging.error("database call failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if car_model is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return car_model


@app.post("/cars", response_model=schemas.Car)
async def create_car(
    car: schemas.CarCreate,
    cars_sql_data: CarsSqlDataType,
    notify: NotifyType,
) -> models.Car:
    try:
        created_car = cars_sql_data.create_car(car)
        notify_status = notify(
            "broker@somedomain.com", f"Added car with id {created_car.id}"
        )
        if notify_status == "received":
            return created_car
        raise Exception("unable to notify")
    except Exception as exc:
        logging.error("database call failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.put("/cars/{car_id}", response_model=schemas.Car)
async def replace_car(
    car_id: int, car: schemas.Car, cars_sql_data: CarsSqlDataType
) -> models.Car:
    if car_id < 1:
        raise HTTPException(status_code=400, detail="Invalid car id")

    if car_id != car.id:
        raise HTTPException(status_code=400, detail="Car id mismatch")

    try:
        car_model = cars_sql_data.update_car(car)
    except Exception as exc:
        logging.error("database call failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    car_model = cars_sql_data.update_car(car)

    if car_model is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return car_model


class InvalidCarIdError(Exception): ...


class CarNotFoundError(Exception): ...


class UnableToNotifyError(Exception): ...


@app.delete("/cars/{car_id}", response_model=schemas.Car)
async def delete_car(
    car_id: int,
    cars_sql_data: CarsSqlDataType,
    notify: NotifyType,
) -> models.Car:
    try:
        if car_id < 1:
            raise InvalidCarIdError(car_id)

        car_model = cars_sql_data.delete_car(car_id)

        if car_model is None:
            raise CarNotFoundError(car_id)

        notify_status = notify(
            "broker@somedomain.com", f"Deleted car with id {car_id}"
        )
        if notify_status != "received":
            raise UnableToNotifyError(notify_status)

        return car_model
    except InvalidCarIdError:
        raise HTTPException(status_code=400, detail="Invalid car id")
    except CarNotFoundError:
        raise HTTPException(status_code=404, detail="Car not found")
    except Exception as exc:
        logging.error("database call failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")


def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)


if __name__ == "__main__":
    main()

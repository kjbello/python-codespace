from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from services.cars_sql_data import CarsSqlData
from services.messages_sql_data import MessagesSqlData
import models
import schemas
import logging


router = APIRouter(prefix="/cars")

CarsSqlDataType = Annotated[CarsSqlData, Depends(CarsSqlData)]
MessagesSqlDataType = Annotated[MessagesSqlData, Depends(MessagesSqlData)]


@router.get("/", response_model=list[schemas.Car])
async def all_cars(
    cars_sql_data: CarsSqlDataType,
) -> list[models.Car]:
    try:
        return cars_sql_data.get_cars()
    except Exception as exc:
        logging.error("database call failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{car_id}", response_model=schemas.Car)
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


@router.post("/", response_model=schemas.Car)
async def create_car(
    car: schemas.CarCreate,
    cars_sql_data: CarsSqlDataType,
    messages_sql_data: MessagesSqlDataType,
) -> models.Car:
    try:
        created_car = cars_sql_data.create_car(car)

        messages_sql_data.create_message(
            schemas.MessageCreate(
                recipient_email="broker@somedomain.com",
                message=f"Added car with id {created_car.id}",
            )
        )
        return created_car
    except Exception as exc:
        logging.error("database call failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{car_id}", response_model=schemas.Car)
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


@router.delete("/{car_id}", response_model=schemas.Car)
async def delete_car(
    car_id: int,
    cars_sql_data: CarsSqlDataType,
    messages_sql_data: MessagesSqlDataType,
) -> models.Car:
    try:
        if car_id < 1:
            raise InvalidCarIdError(car_id)

        car_model = cars_sql_data.delete_car(car_id)

        if car_model is None:
            raise CarNotFoundError(car_id)

        messages_sql_data.create_message(
            schemas.MessageCreate(
                recipient_email="broker@somedomain.com",
                message=f"Removed car with id {car_id}",
            )
        )

        return car_model
    except InvalidCarIdError:
        raise HTTPException(status_code=400, detail="Invalid car id")
    except CarNotFoundError:
        raise HTTPException(status_code=404, detail="Car not found")
    except Exception as exc:
        logging.error("database call failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")
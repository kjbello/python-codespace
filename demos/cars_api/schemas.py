from pydantic import BaseModel


class BaseCar(BaseModel):
    make: str
    model: str
    year: int
    color: str
    price: float


class CarCreate(BaseCar):
    pass


class Car(BaseCar):
    id: int

    # talk about this later
    class Config:
        # from_orm = True
        from_attributes = True

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


class BaseColor(BaseModel):
    name: str
    hex_code: str


class ColorCreate(BaseColor):
    pass


class Color(BaseColor):
    id: int

    # talk about this later
    class Config:
        # from_orm = True
        from_attributes = True

class BaseMessage(BaseModel):
    recipient_email: str
    message: str

class MessageCreate(BaseMessage):
    pass

class Message(BaseMessage):
    id: int

    # talk about this later
    class Config:
        # from_orm = True
        from_attributes = True

class NotifyResponse(BaseModel):
    status: str
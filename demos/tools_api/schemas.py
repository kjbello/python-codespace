from pydantic import BaseModel, field_validator
import re


class BaseCar(BaseModel):
    make: str
    model: str
    year: int
    color: str
    price: float

    @field_validator("year")
    @classmethod
    def validate_year(cls, value: int) -> int:
        if value <= 1886:
            raise ValueError("year cannot be earlier than or equal to 1886- the year the car was invented")
        return value

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: float) -> float:
        if value <= 0.00:
            raise ValueError("price cannot be less or equal to zero")
        return value

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

    @field_validator("name", "hex_code")
    @classmethod
    def validate_required(cls, value: str) -> str:
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("is required")
        return value

    @field_validator("hex_code")
    @classmethod
    def validate_hex_code(cls, value: str) -> str:
        if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", value):
            raise ValueError("not a valid CSS hexcode")
        return value.lower()


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
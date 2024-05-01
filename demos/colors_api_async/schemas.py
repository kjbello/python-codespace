from pydantic import BaseModel


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

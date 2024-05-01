from pydantic import BaseModel


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

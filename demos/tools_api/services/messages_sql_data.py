# crud - create, read, update, and delete
from fastapi import Depends
from sqlalchemy.orm import Session
import time
from threading import currentThread

import models
import schemas

from services.get_db_session import get_db_session


class MessagesSqlData:
    def __init__(self, db_session: Session = Depends(get_db_session)) -> None:
        self.__db_session = db_session

    def create_message(self, message: schemas.MessageCreate) -> models.Message:
        print(f"background thread: {currentThread().native_id}")
        print("waiting to save message")
        time.sleep(5)
        print("saving message")
        message_model = models.Message(
            recipient_email=message.recipient_email,
            message=message.message,
        )
        self.__db_session.add(message_model)
        self.__db_session.commit()
        self.__db_session.refresh(message_model)
        return message_model

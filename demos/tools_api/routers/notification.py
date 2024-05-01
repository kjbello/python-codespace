from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Annotated
from threading import currentThread
import logging

from services.messages_sql_data import MessagesSqlData
import models
import schemas
from database import engine

models.Base.metadata.create_all(bind=engine)


router = APIRouter()

MessagesSqlDataType = Annotated[MessagesSqlData, Depends(MessagesSqlData)]


@router.post("/notify", response_model=schemas.NotifyResponse)
async def create_message(
    message: schemas.MessageCreate,
    messages_sql_data: MessagesSqlDataType,
    background_tasks: BackgroundTasks,
) -> dict[str, str]:
    try:
        print(f"connection thread: {currentThread().native_id}")
        background_tasks.add_task(messages_sql_data.create_message, message)
        return {"status": "received"}
    except Exception as exc:
        logging.error("notify failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")
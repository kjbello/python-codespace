from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from typing import Annotated
from threading import currentThread
import uvicorn
import logging

from services.messages_sql_data import MessagesSqlData
import models
import schemas
from database import engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

MessagesSqlDataType = Annotated[MessagesSqlData, Depends(MessagesSqlData)]


@app.post("/notify", response_model=schemas.NotifyResponse)
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


def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8001)


if __name__ == "__main__":
    main()

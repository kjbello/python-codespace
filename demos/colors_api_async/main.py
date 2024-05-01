from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated, AsyncGenerator, Any
import uvicorn

from services.colors_sql_data import ColorsSqlData
import models
import schemas
from database import sessionmanager
# from database import engine

# ensures all tables are created
# models.Base.metadata.create_all(bind=engine)

import logging


# the purpose of this lifespan function to create (and possibly delete)
# the table
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("start lifespan")
    if sessionmanager.engine is None:
        raise Exception("Database engine is not initialized")
    async with sessionmanager.engine.begin() as conn:
        # await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)
    yield  # yields back FastAPI to handle requests from clients
    if sessionmanager.engine is not None:
        # Close the DB connection
        await sessionmanager.close()
    print("end lifespan")


app = FastAPI(lifespan=lifespan)


ColorsSqlDataType = Annotated[ColorsSqlData, Depends(ColorsSqlData)]


@app.get("/colors", response_model=list[schemas.Color])
async def all_colors(
    colors_sql_data: ColorsSqlDataType,
) -> list[models.Color]:
    return await colors_sql_data.get_colors()


# Common Http Status Codes
# 200-level - Success
#   200 - Ok
#   201 - Created
#   204 - No Content
# 400-level - User Error
#   400 - Bad Request
#   404 - Not Found
# 500-level - Server Error
#   500 - Internal Server Error


@app.get("/colors/{color_id}", response_model=schemas.Color)
async def one_color(
    color_id: int,
    colors_sql_data: ColorsSqlDataType,
) -> models.Color:
    if color_id < 1:
        raise HTTPException(status_code=400, detail="Invalid color id")

    color_model = await colors_sql_data.get_color(color_id)

    if color_model is None:
        raise HTTPException(status_code=404, detail="Color not found")

    return color_model


@app.post("/colors/bulk", response_model=list[schemas.Color])
async def bulk_create_color(
    colors: list[schemas.ColorCreate],
    colors_sql_data: ColorsSqlDataType,
) -> list[models.Color]:
    return await colors_sql_data.bulk_create_colors(colors)


@app.post("/colors", response_model=schemas.Color)
async def create_color(
    color: schemas.ColorCreate,
    colors_sql_data: ColorsSqlDataType,
) -> models.Color:
    try:
        return await colors_sql_data.create_color(color)
    except Exception as exc:
        logging.error("internal server error for bulk create", exc_info=exc)
        raise HTTPException(500, "Internal Server Error")


@app.put("/colors/{color_id}", response_model=schemas.Color)
async def replace_color(
    color_id: int, color: schemas.Color, colors_sql_data: ColorsSqlDataType
) -> models.Color:
    if color_id < 1:
        raise HTTPException(status_code=400, detail="Invalid color id")

    if color_id != color.id:
        raise HTTPException(status_code=400, detail="Color id mismatch")

    color_model = await colors_sql_data.update_color(color)

    if color_model is None:
        raise HTTPException(status_code=404, detail="Color not found")

    return color_model


@app.delete("/colors/{color_id}", response_model=schemas.Color)
async def delete_color(
    color_id: int,
    colors_sql_data: ColorsSqlDataType,
) -> models.Color:
    if color_id < 1:
        raise HTTPException(status_code=400, detail="Invalid color id")

    color_model = await colors_sql_data.delete_color(color_id)

    if color_model is None:
        raise HTTPException(status_code=404, detail="Color not found")

    return color_model


def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)


if __name__ == "__main__":
    main()

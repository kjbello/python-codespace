# crud - create, read, update, and delete
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import schemas

from services.get_db_session import get_db_session


class ColorsSqlData:
    def __init__(
        self, db_session: AsyncSession = Depends(get_db_session)
    ) -> None:
        self.__db_session = db_session

    async def get_colors(self) -> list[models.Color]:
        stmt = select(models.Color)
        result = await self.__db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_color(self, color_id: int) -> models.Color | None:
        stmt = select(models.Color).where(models.Color.id == color_id)
        result = await self.__db_session.execute(stmt)
        return result.scalars().first()

    async def create_color(self, color: schemas.ColorCreate) -> models.Color:
        color_model = models.Color(name=color.name, hex_code=color.hex_code)
        self.__db_session.add(color_model)
        await self.__db_session.commit()
        await self.__db_session.refresh(color_model)
        return color_model

    async def bulk_create_colors(
        self, colors: list[schemas.ColorCreate]
    ) -> list[models.Color]:
        color_models = [
            models.Color(name=color.name, hex_code=color.hex_code)
            for color in colors
        ]

        self.__db_session.add_all(color_models)
        await self.__db_session.commit()
        for color_model in color_models:
            await self.__db_session.refresh(color_model)

        return color_models

    async def update_color(self, color: schemas.Color) -> models.Color | None:
        color_model = await self.get_color(color.id)
        if color_model is None:
            return None

        color_model.name = color.name
        color_model.hex_code = color.hex_code
        await self.__db_session.commit()
        await self.__db_session.refresh(color_model)
        return color_model

    async def delete_color(self, color_id: int) -> models.Color | None:
        color_model = await self.get_color(color_id)
        if color_model is None:
            return None

        await self.__db_session.delete(color_model)
        await self.__db_session.commit()
        return color_model

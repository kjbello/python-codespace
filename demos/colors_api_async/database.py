import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE_URL = "sqlite+aiosqlite:///./colors_api_async.sqlite3"


class DatabaseSessionManager:
    engine: AsyncEngine | None
    sessionmaker: async_sessionmaker[AsyncSession] | None

    # will run when this module is loaded
    def __init__(self) -> None:
        self.engine = create_async_engine(
            DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
        )
        self.sessionmaker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    # will run when the application exits
    async def close(self) -> None:
        if self.engine is None:
            raise Exception("Database Session Manager is not initialized")
        await self.engine.dispose()

        self.engine = None
        self.sessionmaker = None

    # @contextlib.asynccontextmanager
    # async def connect(self) -> AsyncIterator[AsyncConnection]:
    #     if self.engine is None:
    #         raise Exception("Database Session Manager is not initialized")

    #     async with self.engine.begin() as connection:
    #         try:
    #             yield connection
    #         except Exception:
    #             await connection.rollback()
    #             raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.engine is None or self.sessionmaker is None:
            raise Exception("Database Session Manager is not initialized")

        session = self.sessionmaker()

        try:
            print("begin session")
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
            print("close session")


sessionmanager = DatabaseSessionManager()

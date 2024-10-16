from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from repository.AccessTokenRepository import AccessTokenRepository
from repository.UserRepository import UserRepository
from config import DB_SCHEMA
from db.singletone import SingletonMeta

DATABASE_URL = f"postgresql+asyncpg://root:root@localhost:5432/fastapi"


class Database(metaclass=SingletonMeta):

    def __init__(self, url):
        self.engine = create_async_engine(
            url,
            pool_pre_ping=True,
            echo=True,
        )
        self.async_session_maker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )

    async def get_repository(self, rep: str):
        async with self.async_session_maker() as session:
            repositories = {
                "UserRepository": UserRepository,
                "AccessTokenRepository": AccessTokenRepository,
            }
            yield repositories[rep](session)

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session


db_instance = Database(DATABASE_URL)

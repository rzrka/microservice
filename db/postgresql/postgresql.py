from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from collections.abc import AsyncGenerator
from db.singletone import SingletonMeta

DATABASE_URL = "postgresql+asyncpg://root:root@localhost:5432/fastapi"

class Database(metaclass=SingletonMeta):

    def __init__(self, url):
        self.engine = create_async_engine(url, pool_pre_ping=True)
        self.async_session_maker = async_sessionmaker(self.engine, autocommit=False, autoflush=False, expire_on_commit=False)

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session


db_instance = Database(DATABASE_URL)
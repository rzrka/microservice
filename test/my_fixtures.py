import asyncio
import os
from datetime import date
from enum import Enum
import contextlib

from fastapi import FastAPI
from httpx import AsyncClient
import httpx
from asgi_lifespan import LifespanManager
from pydantic import BaseModel
from schemas.PostSchema import PostRead, PostCreate
from models.PostModel import Post
from server import app
import pytest
import pytest_asyncio
from db.postgresql.postgresql import Database, db_instance
from alembic.config import Config
from alembic import command

DATABASE_URL = f"postgresql+asyncpg://root:root@localhost:5432/test"

class TestDataBase(Database):
    ...

db_test_instance = TestDataBase(DATABASE_URL)

@contextlib.asynccontextmanager
async def lifespan_wrapper(app):
    os.environ["DB_NAME"] = "test"
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option('sqlalchemy.url', "postgresql://root:root@localhost:5432/test")
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")

app.router.lifespan_context = lifespan_wrapper

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client()-> AsyncClient:
    app.dependency_overrides[db_instance.get_async_session] = db_test_instance.get_async_session
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c


@pytest.fixture
def post_valid():
    return dict(
        title="test1",
        content="test1",
        publication_date="2024-10-21T13:44:01.610Z",
    )

@pytest.fixture
def post_invalid():
    return dict(
        title="test1",
        publication_date="2024-10-21T13:44:01.610Z",
    )
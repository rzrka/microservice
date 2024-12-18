import asyncio
import os
from datetime import date
from enum import Enum
import contextlib
from typing import Any

from fastapi import FastAPI
from httpx import AsyncClient
import httpx
from asgi_lifespan import LifespanManager
from httpx_ws.transport import ASGIWebSocketTransport
from pydantic import BaseModel
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from schemas.PostSchema import PostRead, PostCreate
from models.PostModel import Post
from server import app
import pytest
import pytest_asyncio
from db.postgresql.postgresql import Database, db_instance
from server import external_api
from alembic.config import Config
from alembic import command

DATABASE_URL = f"postgresql+asyncpg://root:root@localhost:5432/test"

class TestDataBase(Database):

    def __init__(self, url):
        self.engine = create_async_engine(
            url,
            pool_pre_ping=True,
            echo=True,
            poolclass=NullPool,
        )
        self.async_session_maker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )

class MockExternalAPI:
    mock_data = {
        "products": [
            {
                "id": 1,
                "title": "iPhone 9",
                "description": "An apple mobile which is nothing like apple",
                "thumbnail": "https://i.dummyjson.com/data/products/1/thumbnail.jpg",
            },
        ],
        "total": 1,
        "skip": 0,
        "limit": 30,
    }

    async def __call__(self) -> dict[str, Any]:
        return MockExternalAPI.mock_data


db_test_instance = TestDataBase(DATABASE_URL)

@contextlib.asynccontextmanager
async def lifespan_wrapper(app):
    yield

app.router.lifespan_context = lifespan_wrapper

@pytest.fixture(autouse=True)
def setup_db():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option('sqlalchemy.url', "postgresql://root:root@localhost:5432/test")
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")


@pytest_asyncio.fixture
async def get_session():
    yield db_test_instance.get_async_session()

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client()-> AsyncClient:
    app.dependency_overrides[db_instance.get_async_session] = db_test_instance.get_async_session
    app.dependency_overrides[external_api] = MockExternalAPI()
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c

@pytest_asyncio.fixture
async def client_ws():
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            transport=ASGIWebSocketTransport(app), base_url="http://app.io"
        ) as test_client:
            yield test_client

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

@pytest_asyncio.fixture(autouse=True)
async def initial_posts(setup_db):
    initial_posts = [
        Post(title="Post 1", content="Content 1"),
        Post(title="Post 2", content="Content 2"),
        Post(title="Post 3", content="Content 3"),
    ]

    async for session in db_test_instance.get_async_session():
        session.add_all(initial_posts)
        await session.commit()

    return initial_posts

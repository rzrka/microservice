import asyncio
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

@contextlib.asynccontextmanager
async def lifespan_wrapper(app):
    print("sub startup")
    yield
    print("sub shutdown")

app.router.lifespan_context = lifespan_wrapper

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def client()-> AsyncClient:
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
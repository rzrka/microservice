import asyncio

import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import status
from pytest_asyncio import fixture
from server import app
from test.my_fixtures import client

@pytest.mark.asyncio
async def test_hello_world(client: httpx.AsyncClient):
    response = await client.get("/test")
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json == {"hello": "world"}
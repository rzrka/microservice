import asyncio

import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import status
from pytest_asyncio import fixture
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_201_CREATED

from server import app
from test.my_fixtures import post_valid, client, post_invalid


@pytest.mark.asyncio
class TestCreatePerson:

    async def test_invalid(self, post:dict, client: httpx.AsyncClient):
        response = await client.post("/posts/new", json=post)
        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid(self, post_valid:dict, client: httpx.AsyncClient):
        response = await client.post("/posts/new", json=post_valid)
        assert response.status_code == HTTP_201_CREATED
        json = response.json()

import asyncio
from typing import Any

import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import status
from test.my_fixtures import client, MockExternalAPI

@pytest.mark.asyncio
async def test_get_products(client: httpx.AsyncClient):
    response = await client.get("/products")

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert json == MockExternalAPI.mock_data
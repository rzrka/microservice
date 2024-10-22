import httpx
import pytest
from fastapi import status

from test.my_fixtures import client


@pytest.mark.asyncio
async def test_hello_world(client: httpx.AsyncClient):
    response = await client.get("/test")
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json == {"hello": "world"}

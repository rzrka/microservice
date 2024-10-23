import asyncio

import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx_ws import aconnect_ws
from httpx_ws.transport import ASGIWebSocketTransport

from test.my_fixtures import client_ws

@pytest.mark.asyncio
async def test_websocket_echo(client_ws: httpx.AsyncClient):
    async with aconnect_ws("/ws/single", client_ws) as websocket:
        await websocket.send_text("Hello")

        message = await websocket.receive_text()
        assert message == "Message text was: Hello"
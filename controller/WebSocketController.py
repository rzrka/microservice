import asyncio

from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from entites.MessageEvent import MessageEvent
from repository.BroadcastBrokerRepository import BroadcastBrokerRepository

router = APIRouter(
    prefix="/ws",
    tags=["ws"],
)


async def receive_message(
        websocket: WebSocket,
        username: str,
        repository: BroadcastBrokerRepository,
):
    async for event in repository.get_events():
        message_event = MessageEvent.parse_raw(event.message)
        if message_event.username != username:
            await websocket.send_json(message_event.dict())


async def send_message(websocket: WebSocket,
                       username: str,
                       repository: BroadcastBrokerRepository,
                       ):
    data = await websocket.receive_text()
    event = MessageEvent(username=username, message=data)
    await repository.send_message(event=event)


@router.websocket("")
async def websocket_endpoint(
        websocket: WebSocket,
        username: str = "Anonymous",
):
    repository = BroadcastBrokerRepository()
    await websocket.accept()
    try:
        while True:
            receive_message_task = asyncio.create_task(
                receive_message(websocket, username, repository=repository)
            )
            send_message_task = asyncio.create_task(send_message(websocket, username, repository=repository))
            done, pending = await asyncio.wait(
                {receive_message_task, send_message_task},
                return_when=asyncio.FIRST_COMPLETED,
            )

            for task in pending:
                task.cancel()

            for task in done:
                task.result()
    except WebSocketDisconnect:
        ...

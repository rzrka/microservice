import json
from xml.sax import parse

from fastapi import APIRouter, Request, Cookie
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, APIKeyCookie
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import WebSocketException
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, WS_1008_POLICY_VIOLATION
from starlette.websockets import WebSocket, WebSocketDisconnect

from db.postgresql.postgresql import db_instance
from models.UserModel import User
from models.UserModel import get_expiration_date, generate_token
from repository.AccessTokenRepository import AccessTokenRepository

from entites.AccessToken import AccessToken
from repository.RedisRepository import RedisRepository
from repository.UserRepository import UserRepository
from schemas.UserSchema import UserCreate, UserRead, UserUpdate
from config import API_TOKEN
from utils.password import get_password_hash
from uuid import UUID
from fastapi import Depends, FastAPI, Form, HTTPException, Response, status
from config import TOKEN_COOKIE_NAME, CSRF_TOKEN_SECRET
from datetime import datetime
import asyncio

router = APIRouter(
    prefix="/ws",
    tags=["ws"],
)

async def echo_message(websocket: WebSocket):
    data = await websocket.receive_text()
    await websocket.send_text(f"Message text was: {data}")

async def send_message(websocket: WebSocket):
    await asyncio.sleep(10)
    await websocket.send_text(f"It is: {datetime.utcnow().isoformat()}")


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket,
                             username: str = "Anonymous",
                             ):
    try:
        await websocket.accept()
        try:
            payload = json.loads(await websocket.receive_text())
            token = payload.get("token")
        except json.JSONDecodeError:
            raise WebSocketException

        if token != API_TOKEN:
            raise WebSocketException(WS_1008_POLICY_VIOLATION)
        await websocket.send_text(f"Hello, {username}!")

        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")

    except (WebSocketDisconnect, WebSocketException):
        await websocket.close()
import asyncio
from datetime import datetime
import json

import httpx
from fastapi import FastAPI, Depends, Query, Cookie, WebSocketException
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.util import await_only
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_403_FORBIDDEN, WS_1008_POLICY_VIOLATION
from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette_csrf import CSRFMiddleware
import contextlib
from config import CSRF_TOKEN_SECRET, TOKEN_COOKIE_NAME
from controller.UserController import get_current_user
from models.UserModel import User
from schemas.UserSchema import UserRead
from services.BroadcastBroker import BroadcastBroker
from urls import urls
from db.postgresql.postgresql import db_instance
from db.redis.redis import RedisDb
from config import API_TOKEN

api_key_header = APIKeyHeader(name="Token")
broadcast = BroadcastBroker()
class Pagination:

    def __init__(self, maximum_limit: int = 100):
        self.maximum_limit = maximum_limit

    async def skip_limit(self, skip: int = Query(0, ge=0), limit: int = Query(10, ge=0)) -> tuple[int, int]:
        capped_limit = min(self.maximum_limit, limit)
        return (skip, capped_limit)
    async def page_size(self, page: int = Query(1, ge=1), size: int = Query(10, ge=0)) -> tuple[int, int]:
        capped_size = min(self.maximum_limit, size)
        return (page, capped_size)

app = FastAPI()
# app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["http://localhost:9000"],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#         max_age=-1,
#     )
#
# app.add_middleware(
#     CSRFMiddleware,
#     secret=CSRF_TOKEN_SECRET,
#     sensitive_cookies={TOKEN_COOKIE_NAME},
#     cookie_domain="localhost",
# )


@app.on_event("startup")
async def startup_event():
    app.state.redis = RedisDb().rd
    app.state.http_client = httpx.AsyncClient()
    await broadcast.connect()

@app.on_event("shutdown")
async def shutdown():
    app.state.redis.close()
    await broadcast.disconnect()

for router in urls:
    app.include_router(router)

async def pagination(skip: int = 0, limit: int = 10) -> tuple[int, int]:
    return (skip, limit)

async def api_token(token: str = Depends(APIKeyHeader(name="Token"))):
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@app.get("/")
async def hello(
        p: tuple[int, int] = Depends(pagination),
):
    skip, limit = p
    value = app.state.redis.get("entries")
    if value is None:
        value = {
            "skip": skip,
            "limit": limit,
        }
        data_str = json.dumps(value)
        app.state.redis.set("entries", data_str)

    return json.loads(value)

@app.get("/protected-route", response_model=UserRead)
async def protected_route(user: User = Depends(get_current_user)):
    return user

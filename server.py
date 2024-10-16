from fastapi import FastAPI, Depends, Query
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from controller.UserController import get_current_user
from models.UserModel import User
from schemas.UserSchema import UserRead
from urls import urls
from db.postgresql.postgresql import db_instance

API_TOKEN = "secret_api_token"

api_key_header = APIKeyHeader(name="Token")

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

for router in urls:
    app.include_router(router)

async def pagination(skip: int = 0, limit: int = 10) -> tuple[int, int]:
    return (skip, limit)

async def api_token(token: str = Depends(APIKeyHeader(name="Token"))):
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@app.get("/", dependencies=[Depends(api_token)])
def hello(
        p: tuple[int, int] = Depends(pagination),
):
    skip, limit = p
    return {
        "skip": skip,
        "limit": limit,
    }

@app.get("/protected-route", response_model=UserRead)
async def protected_route(user: User = Depends(get_current_user)):
    return user

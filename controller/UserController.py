from argon2 import hash_password
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgresql.postgresql import db_instance
from models.UserModel import User, AccessToken
from schemas.UserSchema import UserCreate, UserRead
from enum import Enum
from typing import Optional, List, Sequence

from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from db.postgresql.postgresql import db_instance
from fastapi import APIRouter, Response, status, Query, Path, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.PostModel import Post
from schemas.PostSchema import PostRead, PostCreate, PostPartialUpdate, PostBase
from repository.PostRepository import PostRepository
from utils.Pagination import pagination
from datetime import datetime
from uuid import UUID
from utils.password import get_password_hash
from repository.UserRepository import UserRepository
from repository.AccessTokenRepository import AccessTokenRepository
from sqlalchemy import exc, select


router = APIRouter(
    prefix="/user",
    tags=["user"],

)

async def get_user_repository(rep: str = "UserRepository"):
    async for rep in db_instance.get_repository(rep):
        yield rep


async def get_access_token_repository(rep: str = "AccessTokenRepository"):
    async for rep in db_instance.get_repository(rep):
        yield rep


@router.post("/register", status_code=HTTP_201_CREATED, response_model=UserRead)
async def register(
        user_create: UserCreate,
        repository: UserRepository = Depends(get_user_repository),
) -> User:
    password = get_password_hash(user_create.password)
    user = User(
        **user_create.dict(exclude={"password"}), password=password
    )
    try:
        user = await repository.create(user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )
    return user

@router.post("/token")
async def create_token(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    user_repository: UserRepository = Depends(get_user_repository),
    access_token_repository: AccessTokenRepository = Depends(get_access_token_repository),
):
    email = form_data.username
    password = form_data.password
    user = await user_repository.authenticate(email, password)
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    token = await access_token_repository.create_token(user)
    return {
        "access_token": token.access_token,
        "token_type": "bearer",
    }

async def get_current_user(
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="/user/token")),
        repository: AccessTokenRepository = Depends(get_access_token_repository),
) -> User:
    access_token: AccessToken = await repository.get_token(token)
    if access_token is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    return access_token.user
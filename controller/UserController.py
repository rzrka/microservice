from argon2 import hash_password
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgresql.postgresql import db_instance, BaseRepository
from models.UserModel import User
from schemas.UserSchema import UserCreate, UserRead
from enum import Enum
from typing import Optional, List, Sequence

from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

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
from repository import get_repository
from sqlalchemy import exc, select


router = APIRouter(
    prefix="/user",
    tags=["user"],

)

async def get_user_repository(rep: str = "UserRepository"):
    return await get_repository(rep)

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


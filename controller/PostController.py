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



router = APIRouter(
    prefix="/posts",
    tags=["posts"],

)

@router.post("/new", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
        post_create: PostCreate,
        session: AsyncSession = Depends(db_instance.get_async_session)
) -> Post:
    repository = PostRepository(session)
    post = await repository.create(post_create)
    return post

@router.get("/", response_model=list[PostRead])
async def list_posts(
    pagination: tuple[int, int] = Depends(pagination),
    session: AsyncSession = Depends(db_instance.get_async_session),
) -> Sequence[Post]:
    skip, limit = pagination
    repository = PostRepository(session)
    post = await repository.list(skip, limit)
    return post

async def get_post_or_404(
        id: UUID,
        session: AsyncSession = Depends(db_instance.get_async_session)
) -> Post:
    repository = PostRepository(session)
    post = await repository.get(id)

    if post is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    return post

@router.get("/{id}", response_model=PostRead)
async def get_post(post: Post = Depends(get_post_or_404)) -> Post:
    return post

@router.patch("/{id}", response_model=PostRead)
async def update_post(
        post_update: PostPartialUpdate,
        post: Post = Depends(get_post_or_404),
        session: AsyncSession = Depends(db_instance.get_async_session),
)-> Post:

    repository = PostRepository(session)
    post_update_dict = post_update.dict(exclude_unset=True)

    for key, value in post_update_dict.items():
        setattr(post, key, value)

    post = await repository.update(post)

    return post

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
async def delete_post(
        post: Post = Depends(get_post_or_404),
        session: AsyncSession = Depends(db_instance.get_async_session),
) -> None:
    repository = PostRepository(session)
    await repository.delete(post)
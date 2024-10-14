from enum import Enum
from typing import Optional, List, Sequence

from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from db.postgresql.postgresql import db_instance
from fastapi import APIRouter, Response, status, Query, Path, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.PostModel import Post
from models.PostModel import Comment
from schemas.PostSchema import PostRead, PostCreate, PostPartialUpdate

from schemas.CommentSchema import CommentCreate
from repository.PostRepository import PostRepository
from repository.CommentRepository import CommentRepository
from utils.Pagination import pagination

router = APIRouter(
    prefix="/posts/{id}/comments",
    tags=["comments"],

)


async def get_post_or_404(
    id: int, session: AsyncSession = Depends(db_instance.get_async_session)
) -> Post:
    repository = CommentRepository(session)
    comment = await repository.get(id)

    if comment is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    return comment

@router.post("/",response_model=CommentCreate, status_code=HTTP_201_CREATED)
async def create_comment(
        comment_create: CommentCreate,
        post: Post = Depends(get_post_or_404),
        session: AsyncSession = Depends(db_instance.get_async_session),
) -> Comment:
    repository = CommentRepository(session)
    comment = await repository.create(comment_create, post)
    return comment


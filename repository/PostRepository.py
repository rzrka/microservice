from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.PostModel import Post
from schemas.PostSchema import PostCreate


class PostRepository:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, post: PostCreate):
        post = Post(**post.dict(), comments=[])
        self._session.add(post)
        await self._session.commit()
        return post

    async def list(self, skip: int, limit: int) -> Sequence[Post]:
        select_query = (
            select(Post).options(selectinload(Post.comments)).offset(skip).limit(limit)
        )
        posts = await self._session.execute(select_query)

        return posts.scalars().all()

    async def get(self, id: UUID) -> Post:
        select_query = (
            select(Post).options(selectinload(Post.comments)).where(Post.id == id)
        )
        result = await self._session.execute(select_query)
        post = result.scalar_one_or_none()
        return post

    async def update(self, post: Post) -> Post:
        self._session.add(post)

        await self._session.commit()

        return post

    async def delete(self, post: Post) -> None:
        await self._session.delete(post)
        await self._session.commit()


from models.PostModel import Post
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import select
from schemas.PostSchema import PostCreate
from typing import Optional, List, Sequence

class PostRepository:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, post: PostCreate):
        post = Post(**post.dict())
        self._session.add(post)
        await self._session.commit()
        return post

    async def list(self, skip: int, limit: int) -> List[Post]:
        select_query = select(Post).offset(skip).limit(limit)
        posts = await self._session.execute(select_query)

        return posts.scalar().all()

    async def get(self, id: int) -> Post:
        query = select(Post).where(Post.id == id)
        result = await self._session.execute(query)
        post = result.scalar_one_or_none()
        return post

    async def update(self, post: Post) -> Post:
        self._session.add(post)

        await self._session.commit()

        return post

    async def delete(self, post: Post) -> None:
        await self._session.delete(post)
        await self._session.commit()

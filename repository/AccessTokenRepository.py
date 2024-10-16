
import contextlib
from datetime import datetime, timezone
from http.client import HTTPException

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from starlette.status import HTTP_401_UNAUTHORIZED

from repository.BaseRepository import BaseRepository
from models.UserModel import User, AccessToken


class AccessTokenRepository(BaseRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_token(self, token: str) -> AccessToken:
        query = select(AccessToken).where(
            AccessToken.access_token == token,
            AccessToken.expiration_date >= datetime.now(tz=timezone.utc).replace(tzinfo=None),
        )
        result = await self._session.execute(query)
        access_token: AccessToken = result.scalar_one_or_none()

        return access_token



    async def create_token(self, user: User):
        access_token = AccessToken(user=user)
        self._session.add(access_token)
        await self._session.commit()
        return access_token
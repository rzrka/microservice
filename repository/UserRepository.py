
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from repository.BaseRepository import BaseRepository
from models.UserModel import User, AccessToken
from utils.password import verify_password

class UserRepository(BaseRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, user: User):
        self._session.add(user)
        await self._session.commit()

        return user

    async def authenticate(self, email: str, password: str) -> User:
        query = select(User).where(User.email == email)
        result = await self._session.execute(query)
        await self._session.close()
        user: User = result.scalar_one_or_none()

        if user is None:
            return None

        if not verify_password(password, user.password):
            return None

        return user


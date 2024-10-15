from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from db.postgresql.postgresql import BaseRepository
from models.UserModel import User


class UserRepository(BaseRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, user: User):
        self._session.add(user)
        await self._session.commit()

        return user
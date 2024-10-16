from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

class IRepository(ABC):

    @abstractmethod
    def __init__(self):
        ...


class BaseRepository(IRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
from sqlalchemy.orm import DeclarativeBase
from config import settings


class Base(DeclarativeBase):
    ...
    __table_args__ = {'schema': settings.DB_SCHEMA}
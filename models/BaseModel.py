from sqlalchemy.orm import DeclarativeBase
from config import DB_SCHEMA


class Base(DeclarativeBase):
    ...
    __table_args__ = {'schema': DB_SCHEMA}
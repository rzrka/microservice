from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, UUID, String
import uuid

class Base(DeclarativeBase):
    ...

class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String)
    email = Column(String)
    password = Column(String)
from datetime import datetime
from email.policy import default
from sqlalchemy import DateTime, Integer, String, Text, UUID, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, UUID, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid
import secrets
from config import DB_SCHEMA
from models.BaseModel import Base
from datetime import datetime, timedelta, timezone

from datetime import datetime, timezone



class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(1024), index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(1024), nullable=False)


def generate_token() -> str:
    return secrets.token_urlsafe(32)

def get_expiration_date(duration_seconds: int = 86400) -> datetime:
    return datetime.now(tz=timezone.utc) + timedelta(seconds=duration_seconds)


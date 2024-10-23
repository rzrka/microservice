from sqlalchemy import String, UUID
import secrets
import uuid
from datetime import datetime, timezone
from datetime import timedelta

from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from models.BaseModel import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(1024), index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(1024), nullable=False)


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def get_expiration_date(duration_seconds: int = 86400) -> datetime:
    return datetime.now(tz=timezone.utc) + timedelta(seconds=duration_seconds)

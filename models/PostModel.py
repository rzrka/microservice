from datetime import datetime
from email.policy import default

from sqlalchemy import DateTime, Integer, String, Text, UUID, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid


class Base(DeclarativeBase):
    ...


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    publication_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    comments: Mapped[list["Comment"]] = relationship("Comment", cascade="all, delete")


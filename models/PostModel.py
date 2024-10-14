from datetime import datetime
from email.policy import default

from sqlalchemy import DateTime, Integer, String, Text, UUID, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid
from db.postgresql.postgresql import Base
from config import DB_SCHEMA
from datetime import datetime, timezone

class Base(DeclarativeBase):
    ...

class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {'schema': 'public'}

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id: Mapped[int] = mapped_column(ForeignKey("public.posts.id"), nullable=False)
    publication_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="comments")

class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {'schema': 'public'}

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    publication_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    comments: Mapped[list[Comment]] = relationship("Comment", cascade="all, delete")


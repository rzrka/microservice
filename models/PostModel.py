import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.BaseModel import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id: Mapped[int] = mapped_column(ForeignKey("public.posts.id"), nullable=False)
    publication_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="comments")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    publication_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    comments: Mapped[list[Comment]] = relationship("Comment", cascade="all, delete")

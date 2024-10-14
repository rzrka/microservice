from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID

class CommentBase(BaseModel):
    publication_date: datetime = Field(default_factory=datetime.now)
    content: str

    class Config:
        orm_mode = True


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: UUID
    post_id: int
from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from schemas.CommentSchema import CommentRead

class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)
    class Config:
        orm_mode = True

class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: str
    comments: List["CommentRead"]
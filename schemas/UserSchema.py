
from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class UserBaseSchema(BaseModel):
    username: str
    email: str
    password: str


class Image(BaseModel):
    url: str
    alias: str


class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool]
    authors: List[str]
    tags: List[str] = []
    metadata: Dict[str, str] = {"key1": "val1"}
    image: Optional[Image] = None

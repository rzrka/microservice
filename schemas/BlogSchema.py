from pydantic import BaseModel
from typing import Optional, List, Dict

class BaseSchema(BaseModel):
    ...

class ImageSchema(BaseSchema):
    url: str
    alias: str

class BlogSchema(BaseSchema):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    tags: List[str] = []
    metadata: Dict[str, str] = {'key1': 'val1'}
    image: Optional[ImageSchema] = None
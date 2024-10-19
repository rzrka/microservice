from pydantic import BaseModel

class MessageEvent(BaseModel):
    username: str
    message: str
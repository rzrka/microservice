from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    password: str

class UserRead(UserBase):
    id: UUID
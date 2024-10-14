from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from repository.UserRepository import UserRepository
from schemas.UserSchema import UserBaseSchema
from db.postgresql.postgresql import db_instance

router = APIRouter(
    prefix="/user",
    tags=["user", ]
)



# @router.post("/")
# def create_user(user: UserBaseSchema, db: Session = Depends(db_instance.get_db)):
#     repository.create_user(user)

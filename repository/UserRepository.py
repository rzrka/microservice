from sqlalchemy.orm.session import Session
from schemas.UserSchema import UserBaseSchema
from models.UserModel import UserModel
from db.hash import Hash
from db.postgresql.postgresql import db_instance

class UserRepository:

    def __init__(self, db):
        self._db = db_instance

    async def create_user(self, user: UserBaseSchema):
        self._session = await self._db.get_async_session()
        new_user = UserModel(
            username=user.username,
            email=user.email,
            password = Hash().bcrypt(user.password),
        )
        self._db.add(new_user)
        self._db.commit()
        self._db.refresh(new_user)
        return new_user
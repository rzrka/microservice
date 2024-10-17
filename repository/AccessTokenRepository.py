from typing import Optional, Union
import json
from uuid import UUID
from models.UserModel import User
from entites.AccessToken import AccessToken


class AccessTokenRepository:

    def __init__(self, app):
        self._redis = app.state.redis

    def create_token(self, token: AccessToken, user_id:User) -> AccessToken:

        self._redis.set(str(token), json.dumps(str(user_id)))
        self._redis.expire(str(token), token.expire_second)
        return token

    def get_user(self, token: AccessToken) -> UUID:
        user_id = self._redis.get(str(token))
        if user_id:
            user_id = json.loads(user_id)
            return UUID(user_id)
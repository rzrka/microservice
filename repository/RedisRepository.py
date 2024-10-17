from typing import Optional, Union
import json

class RedisRepository:


    def __init__(self, app):
        self._connection = app.state.redis


    def set(self, key: Union[bytes, str, int, float], value, expire_second:int = None):
        self._connection.set(key, json.dumps(value))
        if expire_second != None:
            self._connection.expire(key, expire_second)

    def get(self, key: Union[bytes, str, int, float]):
        value = self._connection.get(key)
        if value:
            value = json.loads(value)
        return value
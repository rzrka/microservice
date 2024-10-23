from redis import Redis
from db.singletone import SingletonMeta
from config import settings
class RedisDb(metaclass=SingletonMeta):

    def __init__(self):
        self.rd = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

    def close(self):
        self.rd.close()
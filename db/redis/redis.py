from redis import Redis
from db.singletone import SingletonMeta

class RedisDb(metaclass=SingletonMeta):

    def __init__(self):
        self.rd = Redis(host="localhost", port=6379, db=0)

    def close(self):
        self.rd.close()
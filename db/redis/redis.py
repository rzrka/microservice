from redis import Redis


class RedisDb:

    def __init__(self):
        self.rd = Redis(host="localhost", port=6379, db=0)

    def close(self):
        self.rd.close()
from broadcaster import Broadcast

from db.singletone import SingletonMeta
from config import settings

class BroadcastBroker(metaclass=SingletonMeta):
    CHANNEL = "CHAT"

    def __init__(self):
        self.broadcast = Broadcast(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")

    async def connect(self):
        await self.broadcast.connect()

    async def disconnect(self):
        await self.broadcast.disconnect()

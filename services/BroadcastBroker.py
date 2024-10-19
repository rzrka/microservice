from broadcaster import Broadcast

from db.singletone import SingletonMeta


class BroadcastBroker(metaclass=SingletonMeta):
    CHANNEL = "CHAT"

    def __init__(self):
        self.broadcast = Broadcast("redis://localhost:6379")

    async def connect(self):
        await self.broadcast.connect()

    async def disconnect(self):
        await self.broadcast.disconnect()

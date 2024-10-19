from services.BroadcastBroker import BroadcastBroker


class BroadcastBrokerRepository:

    def __init__(self):
        self.broker = BroadcastBroker()
        self.broadcast = self.broker.broadcast
        self.channel = self.broker.CHANNEL

    async def send_message(self, event):
        await self.broadcast.publish(channel=self.channel, message=event.json())

    async def get_events(self):
        async with self.broadcast.subscribe(channel=self.channel) as subscriber:
            async for event in subscriber:
                yield event

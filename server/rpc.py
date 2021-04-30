import json
import uuid
from aio_pika import connect, IncomingMessage, Message


class RPC:
    def __init__(self, loop):
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}
        self.loop = loop

    async def connect(self):
        self.connection = await connect("amqp://guest:guest@172.17.0.2/", loop=self.loop)
        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.consume(self.on_response)

    def on_response(self, message: IncomingMessage):
        future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)

    async def request(self, task):
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()

        data = json.dumps(task).encode('utf-8')

        self.futures[correlation_id] = future

        await self.channel.default_exchange.publish(
            Message(data,
                    content_type="text/plain",
                    correlation_id=correlation_id,
                    reply_to=self.callback_queue.name),
            routing_key="rpc_queue",
        )

        reply = await future
        return json.loads(reply.decode('utf-8'))


async def setup_rabbit(loop):
    rpc = RPC(loop)
    await rpc.connect()
    return rpc

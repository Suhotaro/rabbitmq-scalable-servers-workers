import asyncio
from functools import partial
from aio_pika import connect, IncomingMessage, Exchange, Message
import json


def add(first_value, second_value):
    return first_value + second_value


async def on_message(exchange: Exchange, message: IncomingMessage):
    with message.process():
        task = json.loads(message.body.decode('utf-8'))

        if task['id'] == "add":
            response = add(task["arg1"], task["arg2"])

        await exchange.publish(
            Message(
                body=json.dumps(response).encode('utf-8'),
                correlation_id=message.correlation_id
            ),
            routing_key=message.reply_to,
        )
        print("Request complete")


async def main(loop):
    connection = await connect("amqp://guest:guest@localhost/", loop=loop)

    channel = await connection.channel()
    queue = await channel.declare_queue("rpc_queue")

    await queue.consume(partial(on_message, channel.default_exchange))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    print(" [x] Awaiting RPC requests")
    loop.run_forever()
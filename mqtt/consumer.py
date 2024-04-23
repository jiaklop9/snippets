#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import asyncio
import time

import aio_pika
from aio_pika.abc import AbstractIncomingMessage


async def on_message(message: AbstractIncomingMessage) -> None:
    """
    on_message doesn't necessarily have to be defined as async.
    Here it is to show that it's possible.
    """
    print(" [x] Received message %r" % message)
    print("Message body is: %r" % message.body)


async def main() -> None:
    # Perform connection
    connection = await aio_pika.connect_robust(
        host='172.16.13.129',
        port=5672,
        login='admin',
        password='123456',
        loop=asyncio.get_event_loop(),
        # 重试间隔
        reconnect_interval=5

    )
    async with connection:
        print('连接成功...')
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue("executeTaskQueue", durable=True)

        # Start listening the queue with name 'hello'
        await queue.consume(on_message, no_ack=False)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
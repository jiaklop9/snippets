#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import asyncio

from aio_pika import Message, connect_robust


async def main() -> None:
    # Perform connection
    connection = await connect_robust(
        host='172.16.13.129',
        port=5672,
        login='admin',
        password='123456',
        loop=asyncio.get_event_loop()
    )
    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue("executeTaskQueue", durable=True)

        # Sending the message
        await channel.default_exchange.publish(
            # Message(b"Hello World!"),
            Message(b"Hello 555!"),
            routing_key=queue.name,
        )

        print(" [x] Sent 'Hello 555!'")


if __name__ == "__main__":
    asyncio.run(main())

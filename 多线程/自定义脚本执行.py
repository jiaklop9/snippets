#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import time
import asyncio
import sys
# from asyncio.exceptions import

"""
1. 脚本不能有空格问题
"""


async def run_code(code_str):
    code_file = f"{str(time.time() * 1000).split('.')[0]}.py"
    with open(code_file, 'w', encoding='utf-8') as file:
        file.write(code_str)

    proc = await asyncio.create_subprocess_exec(
        sys.executable, code_file,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    print(f'stdout: {stdout}')
    print(f'stderr: {stderr}')
    # Wait for the subprocess exit.
    await proc.wait()
    os.remove(code_file)
    return stdout, stderr


if __name__ == '__main__':
    # https://stackoverflow.com/questions/44633458/why-am-i-getting-notimplementederror-with-async-and-await-on-windows
    if 'win32' in sys.platform:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    print('start...')
    code = """
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
        password='admin',
        loop=asyncio.get_event_loop()
    )
    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue("test", durable=True)

        # Sending the message
        await channel.default_exchange.publish(
            # Message(b"Hello World!"),
            Message(b"Hello 555!"),
            routing_key=queue.name,
        )

        print(" [x] Sent 'Hello 555!'")


if __name__ == "__main__":
    asyncio.run(main())

    """
    date = asyncio.run(run_code(code))
    # print(f"Current date: {date}")

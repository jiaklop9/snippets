#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import asyncio
from asyncio import StreamReader, StreamWriter


class ServerStatus(object):
    def __init__(self):
        self._writers = list()

    async def _echo(self, reader: StreamReader, writer: StreamWriter):
        try:

            while (data := await reader.readline()) != b'':
                writer.write(data)
                await writer.drain()
            self._writers.remove(writer)
            await self._notify_all(f'Client disconnected, {len(self._writers)} user(s) are online!')
        except Exception as e:
            print(f"Error while reading from client: {e}")
            self._writers.remove(writer)

    async def _notify_all(self, msg):
        for writer in self._writers:
            try:
                writer.write(msg.encode())
                await writer.drain()
            except ConnectionError as e:
                print(f"Could not connect to client: {e}")
                self._writers.remove(writer)

    async def _on_connect(self, writer: StreamWriter):
        self._writers.append(writer)
        writer.write(f"Welcome! {len(self._writers)} user(s) are online!".encode())
        # 阻塞写入，直到队列中数据处理完成后，该命令才写入，目的：防止内存爆炸
        await writer.drain()
        await self._notify_all("New user connected!")

    async def add_client(self, reader: StreamReader, writer: StreamWriter):
        await self._on_connect(writer)
        await self._echo(reader, writer)


async def main():
    server_state = ServerStatus()

    async def client_connected(reader, writer):
        await server_state.add_client(reader, writer)

    server = await asyncio.start_server(client_connected, 'localhost', 8080)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())



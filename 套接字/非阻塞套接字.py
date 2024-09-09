#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import select
import selectors
import socket
import time
from selectors import SelectorKey
from typing import List, Tuple


def is_connection(sock):
    r, w, e = select.select([], [sock], [], 0)
    print(f'r: {r}, w: {w}, e: {e}')
    return sock in w


selector = selectors.DefaultSelector()
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


server_address = ('localhost', 8080)
server_socket.setblocking(False)
server_socket.bind(server_address)
server_socket.listen()

selector.register(server_socket, selectors.EVENT_READ)


while True:
    # 创建一秒后超时的选择器
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)
    print(time.time())
    if len(events) == 0:
        print(f"No events, waiting for connection")

    for event, _ in events:
        # 获取事件的套接字
        event_socket = event.fileobj
        # 事件套接字与服务端套接字相同，证明是一次连接尝试
        if event_socket == server_socket:
            connection, address = event_socket.accept()
            connection.setblocking(False)
            print(f"Connection from: {address}")
            selector.register(connection, selectors.EVENT_READ)
        else:
            if is_connection(event_socket):
                data = event_socket.recv(1024)
                print(f"I got some data: {data}")
                event_socket.send(data)
            else:
                break




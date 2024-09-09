#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import socket
import time

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


server_address = ('localhost', 8000)
socket_server.bind(server_address)
socket_server.listen()
socket_server.setblocking(False)
print('start listening...')

try:
    connection, client_address = socket_server.accept()
    print(f"I get connection from: {client_address}")

    buffer = connection.recv(1024)
    while buffer[-2:] != b'\r\n':
        data = connection.recv(2)
        if not data:
            break
        else:
            print(f"I get data: {data}")
            buffer = buffer + data
    print(f"All the data is : {buffer}")
finally:
    socket_server.close()




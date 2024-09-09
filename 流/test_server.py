#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import socket
import time


def main():
    # 创建一个socket对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接到服务器
    server_address = ('127.0.0.1', 8080)
    client_socket.connect(server_address)

    try:
        # 发送数据
        message = 'Hello, Server!'
        client_socket.sendall(message.encode())

        # 接收数据
        data = client_socket.recv(1024)
        print('Received from server:', data.decode())
        time.sleep(100)

    finally:
        # 关闭socket连接
        client_socket.close()


if __name__ == '__main__':
    main()

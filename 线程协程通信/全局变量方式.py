#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import threading
import asyncio

# 定义一个全局变量
global_var = 0


# 定义一个协程函数，用于修改全局变量的值
async def coroutine():
    global global_var
    for i in range(10):
        await asyncio.sleep(1)  # 模拟异步操作
        global_var += 1
        print("协程修改了全局变量的值为：", global_var)


# 定义一个线程函数，用于读取全局变量的值
def thread_func():
    global global_var
    for i in range(10):
        threading.Event().wait(1)  # 模拟阻塞操作
        print("线程读取到全局变量的值为：", global_var)


# 创建协程对象
coro = coroutine()

# 创建线程对象
thread = threading.Thread(target=thread_func)

# 启动协程和线程
asyncio.run(coro)
thread.start()

# 等待线程执行完毕
thread.join()

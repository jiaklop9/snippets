#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import asyncio
import time

"""
相比装饰器来说对代码的入侵性比较大，不易于修改，好处是使用起来比较灵活，不用写过多的重复代码
"""


class CostTime(object):
    def __init__(self):
        self.t = 0

    def __enter__(self):
        self.t = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"cost time {time.perf_counter() - self.t:.8f} seconds")


def test():
    print('func start')
    with CostTime():
        time.sleep(2)
        print('func end')


async def test_async():
    print('async func start')
    with CostTime():
        await asyncio.sleep(2)
        print('async func end')


if __name__ == '__main__':
    test()
    asyncio.get_event_loop().run_until_complete(test_async())

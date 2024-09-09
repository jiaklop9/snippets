#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import asyncio
import time
from asyncio.coroutines import iscoroutinefunction


"""
优点：使用装饰器来统计函数执行耗时的好处是对函数的入侵性小，易于编写和修改。
缺点：装饰器装饰函数的方案只适用于统计函数的运行耗时，如果有代码块耗时统计的需求就不能用了，这种情况下我们可以使用 with 语句自动管理上下文
"""


def cost_time(func):
    def func_wrapper(*args, **kwargs):
        t = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"function {func.__name__} cost time {time.perf_counter() - t:.8f} seconds")
        return result

    async def func_wrapper_async(*args, **kwargs):
        t = time.perf_counter()
        result = await func(*args, **kwargs)
        print(f"function {func.__name__} cost time {time.perf_counter() - t:.8f} seconds")
        return result

    if iscoroutinefunction(func):
        return func_wrapper_async
    return func_wrapper


@cost_time
def test():
    print('func start')
    time.sleep(2)
    print('func end')


@cost_time
async def test_async():
    print('async func start')
    await asyncio.sleep(2)
    print('async func end')


if __name__ == '__main__':
    test()
    asyncio.get_event_loop().run_until_complete(test_async())

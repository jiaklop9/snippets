#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import concurrent.futures


# 模拟的任务函数
def task_function(task):
    print(f"Processing task: {task}")


# 创建线程池
with concurrent.futures.ThreadPoolExecutor() as executor:
    # 创建一个任务队列
    task_queue = ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"]

    # 提交任务到线程池
    for task in task_queue:
        executor.submit(task_function, task)

    # 等待所有任务完成
    executor.shutdown()
#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
from loguru import logger


def setup_logging():
    # 设置日志格式
    format = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> ' \
              '| <magenta>进程ID:{process}</magenta>:<yellow>线程ID:{thread}</yellow> ' \
              '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<yellow>{line}</yellow> - <level>{message}</level>'

    # 添加控制台处理器
    # logger.add(sys.stderr, format=format)

    # 添加文件处理器，按大小分割，保留7天，压缩为zip文件
    # enqueue: 启用异步写日志
    # diagnose: 启用诊断模式，显示异常追踪中的变量值
    logger.add(
        sink="test.log",
        rotation="100 MB",
        retention="7 days",
        encoding='utf-8',
        compression="zip",
        enqueue=True,
        diagnose=True,
        catch=True,
        format=format
    )

    # 设置日志级别
    logger.level("INFO")

    # 添加过滤器，仅记录特定模块的日志信息
    # logger.add("filtered.log", filter=lambda record: record["extra"].get("module") == "my_module")

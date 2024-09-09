#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


def check_chinese_char(_str):
    """判断字符串中是否包含中文"""
    for ch in _str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

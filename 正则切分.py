#!/usr/bin/env python3
# -*- coding: utf8 -*-

import re


def main():
    data = "你好，吃饭了吗？要不要一起来点呢！"
    result = re.split(r',|!|！|？', data)
    print(result)


if __name__ == '__main__':
    main()
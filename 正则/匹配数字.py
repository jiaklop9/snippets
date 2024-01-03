#!/usr/env/bin python3
# -*- encoding: utf-8 -*-

import re


def main():
    text = '查询成功，共147条。'
    match = re.search('\d+', text)
    print(int(match.group()))


if __name__ == '__main__':
    main()
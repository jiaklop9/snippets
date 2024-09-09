#!/usr/env/bin python3
# -*- encoding: utf-8 -*-

import re


def main():
    text = '2024年1月'
    match = re.search(r'\d+年\d+月', text)
    print(match)


def draw_msg():
    line = '共 45 条'
    math = re.search(r'共 \d+ 条', line)
    # print(math)
    # print(math.group(0))
    _id = re.findall(r'\d+', math.group(0))[0]
    print(_id)
    print(type(_id))


if __name__ == '__main__':
    # main()
    draw_msg()
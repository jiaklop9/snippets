#!/usr/env/bin python3
# -*- encoding: utf-8 -*-

import re


def main():
    text = '2024年1月'
    match = re.search(r'\d+年\d+月', text)
    print(match)


if __name__ == '__main__':
    main()
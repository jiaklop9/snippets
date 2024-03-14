#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


def main(x):
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    num = 0
    while x > num:
        num = num * 10 + x % 10
        x /= 10
    return x == num or x == num / 10


if __name__ == "__main__":
    main(120)


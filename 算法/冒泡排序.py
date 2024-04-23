#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


def bubble_sort(data_list):
    for i in range(len(data_list) - 1, 0, -1):
        for j in range(i):
            if data_list[j] < data_list[j + 1]:
                tmp = data_list[j]
                data_list[j] = data_list[j+1]
                data_list[j+1] = tmp

    print(data_list)


def bubble_sort_v2(data_list):
    """无数据交换，证明已经是有序的，此时结束"""
    exchange = True
    _length = len(data_list)
    while _length > 0 and exchange:
        for i in range(_length - 1):
            if data_list[i] > data_list[i+1]:
                tmp = data_list[i]
                data_list[i] = data_list[i+1]
                data_list[i+1] = tmp
            else:
                exchange = False
        _length = _length - 1
    print(data_list)


if __name__ == '__main__':
    # bubble_sort(data_list=[0, 1, 2, 3, 4, 5, 6, 7, 10, 99, 13])
    bubble_sort_v2(data_list=[0, 1, 2, 3, 4, 5, 6, 7, 10, 99, 13])

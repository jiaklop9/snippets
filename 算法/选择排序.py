#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

def select_sort(data_list):
    """每次都选择列表中最大的数，进行n-1轮"""
    for index in range(len(data_list)-1, 0, -1):
        max_index = 0
        for loc in range(1, index+1):
            if data_list[loc] > data_list[max_index]:
                max_index = loc

        tmp = data_list[index]
        data_list[index] = data_list[max_index]
        data_list[max_index] = tmp

    print(data_list)


if __name__ == '__main__':
    select_sort([1, 3, 4, 578, 90, 12, 565])

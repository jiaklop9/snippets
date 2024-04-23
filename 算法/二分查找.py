#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

def binary_search(data_list, item):
    first = 0
    last = len(data_list) - 1
    found = False

    while first <= last and not found:
        mid = (first + last) // 2
        if item == data_list[mid]:
            found = True
        else:
            if item < data_list[mid]:
                last = mid - 1
            else:
                first = mid + 1
    return found


def binary_search_recursive(data_list, item):
    if len(data_list) == 0:
        return False
    mid = len(data_list) // 2
    if item == data_list[mid]:
        return True
    if item < data_list[mid]:
        return binary_search_recursive(data_list[:mid], item)
    return binary_search_recursive(data_list[mid+1:], item)


if __name__ == '__main__':
    # result = binary_search([1, 2, 3, 4, 5, 6, 7, 8, 9], 10)
    # print(result)
    result = binary_search_recursive([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 6)
    print(result)
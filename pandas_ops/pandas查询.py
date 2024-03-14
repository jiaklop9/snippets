#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import pandas as pd


def main(df):
    # 查询为空的字段
    result = df.query("name == '' or name.isnan()")
    # 查询特定单元格值
    index = 0
    name = df.loc[index, 'name']
    name, age = df.loc[index, ['name', 'age']]


def test():

    # 假设你有一个名为df的DataFrame
    df = pd.DataFrame({
       'A': [1, 2, 3],
       'B': [4, 5, 6],
       'C': [7, 8, 9]
    })

    # 使用query()函数查询列名称为"A"的行
    # result = df.query('A == 2')
    # print(result)

    result = df.loc[df['A'] == 2]
    if result.empty:
        print('xxxxxx')
    else:
        print('yyyyyy')


if __name__ == '__main__':
    test()


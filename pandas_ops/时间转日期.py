#!/usr/bin/env python3
# -*- coding: utf8 -*-

import pandas as pd


def main():
    # 示例 DataFrame
    data = {'date_column': ['2021-01-01', '2021-02-01', '2021-03-01']}
    df = pd.DataFrame(data)

    # 列名
    column = 'date_column'

    # 检查列是否为 datetime 类型，然后进行相应的处理
    df[column] = df[column].dt.date if pd.api.types.is_datetime64_any_dtype(df[column]) else df[column]

    # 打印结果
    print(df)
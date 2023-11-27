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

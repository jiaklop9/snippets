#!/usr/bin/env python3
# -*- coding: utf8 -*-

import pandas as pd


def main(df):
    # 转换列类型
    for col in ['企业社会信用代码', '集团社会信用代码', '支付单位社会信用代码']:
        if col in df.columns:
            # 转换为str, 但是值为空的，不处理
            df[col] = df[col].astype(str) if pd.notna(df[col]).any() else df[col]
    return df
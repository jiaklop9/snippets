#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import pandas as pd


def main():
    # 创建一个示例 DataFrame（具有多级表头，包含 "Unnamed"）
    data = {'A': [1, 2, 3, 4],
            'B': [5, 6, 7, 8],
            'Unnamed: 0_level_1': ['X', 'Y', 'Z', 'W'],
            'Unnamed: 1_level_1': ['M', 'N', 'O', 'P']}
    df = pd.DataFrame(data)

    level_0_labels = df.columns.get_level_values(0)
    # 获取二级表头的标签
    level_1_labels = df.columns.get_level_values(1)
    # 将二级表头中包含 "Unnamed" 的部分更新为新的标签
    new_level_1_labels = [
        level_0_labels[i] if 'Unnamed' in level_1_labels[i] else level_1_labels[i]
        for i in range(len(level_1_labels))
    ]
    # 处理列表中的重复项
    seen = set()
    result = []
    for item in new_level_1_labels:
        if item in seen:
            result.append(item + ' ')
        else:
            result.append(item)
            seen.add(item)
    # 更新 DataFrame 的列标签
    df.columns = list(zip(level_0_labels, result))
    print(df.columns)


if __name__ == '__main__':
    main()

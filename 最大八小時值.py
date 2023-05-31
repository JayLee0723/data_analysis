# -*- coding: utf-8 -*-
"""
Created on Wed May 31 12:15:05 2023

@author: ajay0
"""

import pandas as pd

# 假设您已经读取了数据并将时间列解析为日期时间类型并设置为索引
df = pd.read_csv(r"C:\Users\ajay0\Desktop\碩論參考文獻\會議新思維\忠明總數據.csv",parse_dates=['time']).set_index('time')
# 按照日期分组
grouped = df.groupby(df.index.date)

# 创建一个空的DataFrame用于存储结果
result = pd.DataFrame()

# 遍历每一天的数据
for date, data in grouped:
    # 按照O3列的值从大到小排序
	sorted_data = data.sort_values(by='O3', ascending=False)
    # 获取最大的前八个小时的数据
	top_eight = sorted_data.head(8)
# 将每天的结果添加到结果DataFrame中
	result = pd.concat([result, top_eight])

# 将结果合并到原始的DataFrame中
df['top_eight_O3'] = result['O3']

df.to_csv('output.csv', index=True)
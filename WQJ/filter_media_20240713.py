import pandas as pd
import json
import os
import csv
def filter_media():
    # 读取第一个csv文件
    df1 = pd.read_csv(r'D:\Documents\WeChat Files\wxid_tte7flosoaz622\FileStorage\File\2024-07\twitter-username-bias-type-1-500(1).csv', dtype=str)

    # 读取第二个csv文件
    df2 = pd.read_csv(r'D:\Documents\WeChat Files\wxid_tte7flosoaz622\FileStorage\File\2024-07\twitter-username-bias-type-原版.csv', dtype=str)


    # 将第一个和第二个csv文件中type列的数据转换为小写
    df1['type'] = df1['type'].str.lower()
    df2['type'] = df2['type'].str.lower()

    # 筛选出第一个csv里type为media的数据
    df1_media = df1[df1['type'] == 'media']

    # 筛选出第二个csv里type为media的数据
    df2_media = df2[df2['type'] == 'media']

    # 找到在第一个csv里type为media，但不在第二个csv里的那些记录
    # 将df2_media的每一行作为一个元组存储在一个集合中
    df2_media_tuples = set(df2_media.apply(tuple, axis=1))

    # 筛选出df1_media中不在df2_media_tuples中的数据
    filtered_result = df1_media[df1_media.apply(tuple, axis=1).map(lambda x: x not in df2_media_tuples)]


    # 保存结果到一个新的csv文件
    filtered_result.to_csv('filtered_media.csv', index=False)

    print("筛选完成，结果已保存到filtered_result.csv")





if __name__ == '__main__':
    # filter_media()

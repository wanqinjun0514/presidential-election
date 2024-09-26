# 文件进行处理，只读取retweet_id、quoted_id、retweeted_origin_full_text字段和quoted_origin_full_text字段。读取每一行文件，retweet_id和quoted_id只会有一个值不为空，或者全为空的情况，不可能出现两个字段都不为空的字段，现在需要将这两个字段不为空的那个值提取出来，构建一个字典，把不为空的字段保存为key，字典里的value是要统计出这个不为空的id在整个csv文件的retweet_id、quoted_id字段里出现了多少次。retweet_id和retweeted_origin_full_text是对应的，id不为空的话，fulltext就不为空。遍历完整个csvb文件之后保存去重统计的数据到新的csv文件里，表头是origin_retweet_id、origin__full_text、count，这三列数据

import pandas as pd
import os
def 单个文件的统计没有问题():
    # 读取 CSV 文件
    file_path = r'F:\three_parts_output\without_url\output_2019_12\2019-12-01-2-output.csv'
    output_file_path = r'F:\Intermediate Results\original_fulltext_and_tweet_id_with_count\processed_2019-12-01-2-output.csv'
    data = pd.read_csv(file_path, dtype=str)

    # 提取需要的字段
    data = data[['retweet_id', 'quoted_id', 'retweeted_origin_full_text', 'quoted_origin_full_text']]

    # 创建字典来统计不为空的 id 及其对应的 full text
    count_dict = {}
    empty_count = 0  # 统计两个字段都为空的情况
    retweet_count = 0
    quoted_count = 0
    # 遍历每一行
    for index, row in data.iterrows():
        if pd.notna(row['retweet_id']):
            key = row['retweet_id']
            full_text = row['retweeted_origin_full_text']
            retweet_count += 1
        elif pd.notna(row['quoted_id']):
            key = row['quoted_id']
            full_text = row['quoted_origin_full_text']
            quoted_count += 1
        else:
            empty_count += 1  # 统计两个字段都为空的情况
            continue  # 如果两个字段都为空，跳过

        if key not in count_dict:
            count_dict[key] = {'full_text': full_text, 'count': 0}

        count_dict[key]['count'] += 1

    # 将结果转换为 DataFrame
    result = pd.DataFrame({
        'origin_retweet_id': [],
        'origin_full_text': [],
        'count': []
    })

    for key, value in count_dict.items():
        result = result._append({
            'origin_retweet_id': key,
            'origin_full_text': value['full_text'],
            'count': value['count']
        }, ignore_index=True)

    # 保存到新的 CSV 文件
    result.to_csv(output_file_path, index=False)
    print(f"{file_path}文件里的原帖被转发的情况总共出现了 {retweet_count} 次。")
    print(f"{file_path}文件里的原帖被引用的情况总共出现了 {quoted_count} 次。")
    print(f"{file_path}文件里的retweet_id和quoted_id字段都为空的情况总共出现了 {empty_count} 次。")
    total_count = retweet_count + quoted_count + empty_count
    print(f"{file_path}文件里的推文一共有 {total_count}")
    print("处理完成，结果已保存到", output_file_path)


# 设置文件夹路径和输出文件路径
input_folder = r'F:\three_parts_output\without_url\output_2019_12'
output_file_path = r'F:\Intermediate Results\original_fulltext_and_tweet_id_with_count\processed_output.csv'
stats_file_path = r'F:\Intermediate Results\original_fulltext_and_tweet_id_with_count\statistics.txt'

# 初始化字典和计数器
count_dict = {}
statistics = []  # 用于存储每个文件的统计信息

# 遍历文件夹中的所有 CSV 文件
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_folder, file_name)
        data = pd.read_csv(file_path, dtype=str)
        print(f'正在读取文件{file_path}')
        # 提取需要的字段
        data = data[['retweet_id', 'quoted_id', 'retweeted_origin_full_text', 'quoted_origin_full_text']]

        # 统计每个文件的情况
        empty_count = 0
        retweet_count = 0
        quoted_count = 0

        # 遍历每一行
        for index, row in data.iterrows():
            if pd.notna(row['retweet_id']):
                key = row['retweet_id']
                full_text = row['retweeted_origin_full_text']
                retweet_count += 1
            elif pd.notna(row['quoted_id']):
                key = row['quoted_id']
                full_text = row['quoted_origin_full_text']
                quoted_count += 1
            else:
                empty_count += 1  # 统计两个字段都为空的情况
                continue  # 如果两个字段都为空，跳过

            # 记录不重复的原帖
            if key not in count_dict:
                count_dict[key] = {'full_text': full_text, 'count': 0}

            count_dict[key]['count'] += 1

        # 将每个文件的统计信息添加到列表
        statistics.append({
            'file_name': file_name,
            'retweet_count': retweet_count,
            'quoted_count': quoted_count,
            'empty_count': empty_count
        })

# 将结果转换为 DataFrame
result = pd.DataFrame({
    'origin_retweet_id': [],
    'origin_full_text': [],
    'count': []
})

for key, value in count_dict.items():
    result = result.append({
        'origin_retweet_id': key,
        'origin_full_text': value['full_text'],
        'count': value['count']
    }, ignore_index=True)

# 保存去重统计的数据到新的 CSV 文件
result.to_csv(output_file_path, index=False)

# 保存统计信息到文本文件
with open(stats_file_path, 'w') as f:
    for stat in statistics:
        f.write(f"文件: {stat['file_name']}, 被转发次数: {stat['retweet_count']}, 被引用次数: {stat['quoted_count']}, 两个字段都为空的次数: {stat['empty_count']}\n")

print(f"处理完成，结果已保存到 {output_file_path} 和 {stats_file_path}")




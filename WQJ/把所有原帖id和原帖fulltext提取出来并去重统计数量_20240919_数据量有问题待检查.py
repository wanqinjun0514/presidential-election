import os
import pandas as pd
month = '2019_12'
# 定义文件夹路径
input_folder = rf'F:\us-presidential-output\output_{month}'

# 创建一个空的DataFrame来存储所有去重后的数据
all_data = pd.DataFrame(columns=['retweet_id', 'retweeted_origin_full_text', 'retweet_id_count'])

# 遍历文件夹中的所有CSV文件
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_folder, file_name)

        # 读取当前CSV文件中的retweet_id和retweeted_origin_full_text列
        df = pd.read_csv(file_path, usecols=['retweet_id', 'retweeted_origin_full_text'],dtype=str)

        # 对当前CSV文件的数据根据retweet_id去重
        df = df.drop_duplicates(subset=['retweet_id', 'retweeted_origin_full_text'])

        # 统计retweet_id出现的次数
        df['retweet_id_count'] = df.groupby('retweet_id')['retweet_id'].transform('count')

        # 将当前CSV的数据添加到总的DataFrame中
        all_data = pd.concat([all_data, df], ignore_index=True)

# 对所有数据根据retweet_id去重，并统计出现的次数总和
final_data = all_data.groupby(['retweet_id', 'retweeted_origin_full_text'], as_index=False).agg(
    {'retweet_id_count': 'sum'})

# 将结果保存到新的CSV文件
output_file = rf'F:\Intermediate Results\original_fulltext_and_tweet_id_spacy_drop_duplicate\20240919\unique_retweet_id_and_fulltext_with_count_{month}.csv'
final_data.to_csv(output_file, index=False)


import os
import pandas as pd
from glob import glob

# 用政客标签提取出相关的简化的转发关系（只筛选和打了标签的政客相关的转贴或者引用用户），只保留四列数据（转发用户id、转发用户名、原帖用户id、原帖用户名）
# 以前的代码是遍历文件每行数据里的retweet_origin_user_id列在politician_user_ids字典里就将该行的'retweeted_user_id', 'retweeted_username', 'retweet_origin_user_id', 'retweet_origin_username'列的信息保存下来，新的csv是这四列数据。
# 但是现在是要修改成遍历文件每行数据里的retweet_origin_user_id和quoted_origin_user_id列这两者之间只要有一个在politician_user_ids字典里，就将该行的'retweeted_user_id', 'retweeted_username','retweet_origin_user_id', 'retweet_origin_username'保存下来（这里需要注意，在保存文件的时候，如果是quoted_origin_user_id列在politician_user_ids字典里，就将quoted_origin_user_id替换掉retweet_origin_user_id，将quoted_origin_username替换掉retweet_origin_username保存在新文件里）
# 这版代码没有考虑到引用的关系
def process_month_old(directory, politician_user_ids):
    # 读取所有输出文件
    output_files = glob(os.path.join(directory, '****-**-**-*-output.csv'))

    # 初始化一个空的 DataFrame 用于存储匹配的转发信息
    matching_politician_df = pd.DataFrame()

    # 处理每个输出文件
    for file in output_files:
        print(f'正在处理{file}')
        df = pd.read_csv(file, dtype=str)


        # 筛选出属于政客的转发信息
        politician_retweets = df[df['retweet_origin_user_id'].isin(politician_user_ids)]

        # 只保留所需的列
        politician_retweets = politician_retweets[
            ['retweeted_user_id', 'retweeted_username', 'retweet_origin_user_id', 'retweet_origin_username']]

        # 追加到结果 DataFrame
        matching_politician_df = pd.concat([matching_politician_df, politician_retweets], ignore_index=True)

    # 保存结果到新的 CSV 文件
    name = os.path.join('F:\Intermediate Results\Simplyfied Forwarding relationship', directory.split('\\')[-1])
    print(name)
    matching_politician_df.to_csv(f'{name}.csv', index=False)
    print(f"已成功筛选并保存政客的转发信息到{name}")




# 这版代码没有考虑到三个部分数据的转发关系不同
def process_month(directory, politician_user_ids):
    # 读取所有输出文件
    output_files = glob(os.path.join(directory, '****-**-**-*-output.csv'))

    # 初始化一个空的 DataFrame 用于存储匹配的转发信息
    matching_politician_df = pd.DataFrame()

    # 处理每个输出文件
    for file in output_files:
        print(f'正在处理{file}')
        df = pd.read_csv(file, dtype=str)

        # 使用矢量化操作来筛选retweet_origin_user_id和quoted_origin_user_id
        retweet_match = df['retweet_origin_user_id'].isin(politician_user_ids)
        quote_match = df['quoted_origin_user_id'].isin(politician_user_ids)

        # 创建一个新的DataFrame，只保留符合条件的行
        matching_retweets = df[retweet_match | quote_match].copy()

        # 如果是quoted_origin_user_id匹配，则替换对应的retweet_origin_user_id和retweet_origin_username
        matching_retweets.loc[quote_match, 'retweet_origin_user_id'] = matching_retweets['quoted_origin_user_id']
        matching_retweets.loc[quote_match, 'retweet_origin_username'] = matching_retweets['quoted_origin_username']

        # 只保留所需的列
        matching_retweets = matching_retweets[
            ['retweeted_user_id', 'retweeted_username', 'retweet_origin_user_id', 'retweet_origin_username']]

        # 追加到结果 DataFrame
        matching_politician_df = pd.concat([matching_politician_df, matching_retweets], ignore_index=True)

        # 保存结果到新的 CSV 文件
    name = os.path.join('F:\Intermediate Results\Simplyfied Forwarding relationship', directory.split('\\')[-1])
    print(name)
    matching_politician_df.to_csv(f'{name}.csv', index=False)
    print(f"已成功筛选并保存政客的转发信息到{name}")








def main():
    # 读取包含政客账号信息的 CSV 文件
    directory = r'F:\us-presidential-output'
    # directory = r'F:\three_parts_output\test'

    combined_df = pd.read_csv(r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\combined_with_screenname_and_bias.csv', dtype=str)
    politician_df = combined_df.dropna(subset=['bias'])
    politician_user_ids = set(politician_df['retweet_origin_user_id'])
    for k in range(2019, 2022):
        for j in range(1, 13):
            if k == 2019 and j < 12:
                continue
            if k == 2021 and j > 2:
                continue
            month = str(j).zfill(2)
            folder = f'output_{k}_{month}'
            folder_path = os.path.join(directory, folder)
            print(folder_path)
            process_month(folder_path, politician_user_ids)
            # return
    # 提取政客的 user_id


main()

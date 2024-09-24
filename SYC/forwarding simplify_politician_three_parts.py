import os
import pandas as pd
from glob import glob
import re

# 这版代码没有考虑到三个部分数据的转发关系不同
# 请帮我修改以下代码，把directory部分改成读取三个文件夹下的以-output.csv结尾的csv文件，三个部分的数据依次是：F:\three_parts_output\without_url、F:\three_parts_output\single_url\external_url、F:\three_parts_output\single_url\twitter_url
# 这三个部分的数据提取出转发关系的方式稍微有一些不同，without_url部分是匹配politician_user_ids没问题，保留四列数据（转发用户id、转发用户名、原帖用户id、原帖用户名），这里的原帖用户id就是唯一标识政客的id了，可以直接输入到奇异值矩阵分解部分进行分解打分
def process_month_without_url(directory, politician_user_ids):
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
    name = os.path.join('F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Politician\without_url', directory.split('\\')[-1])
    print(name)
    matching_politician_df.to_csv(f'{name}.csv', index=False)
    print(f"已成功筛选并保存政客的转发信息到{name}")


def process_without_url_fowarding_relationship_main():
    # 读取包含政客账号信息的 CSV 文件
    # directory = r'F:\us-presidential-output'
    # directory = r'F:\three_parts_output\test'
    directory_without_url = r'F:\three_parts_output\without_url'
    combined_df = pd.read_csv(
        r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\combined_with_screenname_and_bias.csv',
        dtype=str)
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
            folder_path = os.path.join(directory_without_url, folder)
            print(folder_path)
            process_month_without_url(folder_path, politician_user_ids)


# 提取用户名函数
def extract_username(url):
    match = re.search(r"https://twitter.com/([^/]+)/", url)
    if match:
        return match.group(1)
    return None

# twitter_url部分是要提取出twitter.com后面的username再和政客标签里的politician_user_ids进行匹配，保留6列数据（转发用户id、转发用户名、原帖用户id、原帖用户名、匹配的政客username、政客的id-这个字段是从标签文件里获取的）
def process_month_twitter_url(directory, politician_username):
    # 读取所有输出文件
    output_files = glob(os.path.join(directory, '****-**-**-*-output.csv'))

    # 初始化一个空的 DataFrame 用于存储匹配的转发信息
    matching_politician_df = pd.DataFrame()

    # 处理每个输出文件
    for file in output_files:
        print(f'正在处理{file}')
        df = pd.read_csv(file, dtype=str)

        # 提取 retweet_expanded_urls_array 和 quoted_expanded_urls_array 中的用户名
        df['retweet_username'] = df['retweet_expanded_urls_array'].apply(
            lambda x: extract_username(x) if pd.notna(x) else None)
        df['quote_username'] = df['quoted_expanded_urls_array'].apply(
            lambda x: extract_username(x) if pd.notna(x) else None)

        # 使用矢量化操作来匹配政客的用户名
        retweet_match = df['retweet_username'].isin(politician_username)
        quote_match = df['quote_username'].isin(politician_username)

        # 创建一个新的DataFrame，只保留符合条件的行
        matching_retweets = df[retweet_match | quote_match].copy()
        # 添加 retweet_origin_screenname 列，保存匹配到的政客用户名
        matching_retweets['retweet_origin_screenname'] = None
        matching_retweets.loc[retweet_match, 'retweet_origin_screenname'] = matching_retweets['retweet_username']
        matching_retweets.loc[quote_match, 'retweet_origin_screenname'] = matching_retweets['quote_username']

        # 如果是quoted_origin_user_id匹配，则替换对应的retweet_origin_user_id和retweet_origin_username
        matching_retweets.loc[quote_match, 'retweet_origin_user_id'] = matching_retweets['quoted_origin_user_id']
        matching_retweets.loc[quote_match, 'retweet_origin_username'] = matching_retweets['quoted_origin_username']

        # 只保留所需的列,新加了一列retweet_origin_screenname，这列是政客的screenname
        matching_retweets = matching_retweets[
            ['retweeted_user_id', 'retweeted_username', 'retweet_origin_user_id', 'retweet_origin_username',
             'retweet_origin_screenname']]

        # 追加到结果 DataFrame
        matching_politician_df = pd.concat([matching_politician_df, matching_retweets], ignore_index=True)

        # 保存结果到新的 CSV 文件
    name = os.path.join(r'F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Politician\twitter_url', directory.split('\\')[-1])
    print(name)
    matching_politician_df.to_csv(f'{name}.csv', index=False)
    print(f"已成功筛选并保存政客的转发信息到{name}")



def process_twitter_url_fowarding_relationship_main():
    # 读取包含政客账号信息的 CSV 文件
    directory_twitter_url = r'F:\three_parts_output\single_url\twitter_url'
    combined_df = pd.read_csv(
        r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\combined_with_screenname_and_bias.csv',
        dtype=str)
    politician_df = combined_df.dropna(subset=['bias'])
    politician_username = set(politician_df['screen_name'])#这里匹配twitter_url后面的数据需要将原帖用户id改成screenname
    for k in range(2019, 2022):
        for j in range(1, 13):
            if k == 2019 and j < 12:
                continue
            if k == 2021 and j > 2:
                continue
            month = str(j).zfill(2)
            folder = f'output_{k}_{month}'
            folder_path = os.path.join(directory_twitter_url, folder)
            print(folder_path)
            process_month_twitter_url(folder_path, politician_username)

# 提取Domain函数
def extract_domain(url):
    # 处理带有协议的URL（http 或 https），提取主域名
    match = re.search(r"https?://(?:www\.)?([^/]+)", url)
    if match:
        return match.group(1)
    return None

def process_month_external_url(directory, politician_domain):
    # 读取所有输出文件
    output_files = glob(os.path.join(directory, '****-**-**-*-output.csv'))

    # 初始化一个空的 DataFrame 用于存储匹配的转发信息
    matching_politician_df = pd.DataFrame()

    # 处理每个输出文件
    for file in output_files:
        print(f'正在处理{file}')
        df = pd.read_csv(file, dtype=str)

        # 提取 retweet_expanded_urls_array 和 quoted_expanded_urls_array 中的用户名
        df['retweet_media_domain'] = df['retweet_expanded_urls_array'].apply(
            lambda x: extract_domain(x) if pd.notna(x) else None)
        df['quote_media_domain'] = df['quoted_expanded_urls_array'].apply(
            lambda x: extract_domain(x) if pd.notna(x) else None)

        # 使用矢量化操作来匹配政客的用户名
        retweet_match = df['retweet_media_domain'].isin(politician_domain)
        quote_match = df['quote_media_domain'].isin(politician_domain)

        # 创建一个新的DataFrame，只保留符合条件的行
        matching_retweets = df[retweet_match | quote_match].copy()
        # 添加 retweet_origin_screenname 列，保存匹配到的政客用户名
        matching_retweets['retweet_origin_domain'] = None
        matching_retweets.loc[retweet_match, 'retweet_origin_domain'] = matching_retweets['retweet_media_domain']
        matching_retweets.loc[quote_match, 'retweet_origin_domain'] = matching_retweets['quote_media_domain']

        # 如果是quoted_origin_user_id匹配，则替换对应的retweet_origin_user_id和retweet_origin_username
        matching_retweets.loc[quote_match, 'retweet_origin_user_id'] = matching_retweets['quoted_origin_user_id']
        matching_retweets.loc[quote_match, 'retweet_origin_username'] = matching_retweets['quoted_origin_username']

        # 只保留所需的列,新加了一列retweet_origin_screenname，这列是政客的screenname
        matching_retweets = matching_retweets[
            ['retweeted_user_id', 'retweeted_username', 'retweet_origin_user_id', 'retweet_origin_username',
             'retweet_origin_domain']]

        # 追加到结果 DataFrame
        matching_politician_df = pd.concat([matching_politician_df, matching_retweets], ignore_index=True)

        # 保存结果到新的 CSV 文件
    name = os.path.join(r'F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Politician\external_url', directory.split('\\')[-1])
    print(name)
    matching_politician_df.to_csv(f'{name}.csv', index=False)
    print(f"已成功筛选并保存政客的转发信息到{name}")

def process_external_url_fowarding_relationship_main():
    # 读取包含政客账号信息的 CSV 文件
    directory_external_url = r'F:\three_parts_output\single_url\external_url'
    combined_df = pd.read_csv(
        r'F:\Experimental Results\Average_Bias_Rating\politician_url_bias.csv',
        dtype=str)
    politician_df = combined_df.dropna(subset=['bias'])
    politician_domain = set(politician_df['Domain'])#这里匹配external_url后面的数据需要将原帖用户id改成Domain
    for k in range(2019, 2022):
        for j in range(1, 13):
            if k == 2019 and j < 12:
                continue
            if k == 2021 and j > 2:
                continue
            month = str(j).zfill(2)
            folder = f'output_{k}_{month}'
            folder_path = os.path.join(directory_external_url, folder)
            print(folder_path)
            process_month_external_url(folder_path, politician_domain)







if __name__ == '__main__':
    # process_without_url_fowarding_relationship_main()
    # process_twitter_url_fowarding_relationship_main()
    process_external_url_fowarding_relationship_main()


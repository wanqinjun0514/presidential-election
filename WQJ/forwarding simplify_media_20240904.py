import os
import pandas as pd
from glob import glob
import re
# 提取Domain函数
def extract_domain(url):
    # 处理带有协议的URL（http 或 https），提取主域名
    match = re.search(r"https?://(?:www\.)?([^/]+)", url)
    if match:
        return match.group(1)
    return None
# 用媒体标签提取出相关的简化的转发关系（只筛选和打了标签的媒体相关的转贴或者引用用户），只保留5列数据（转发用户id、转发用户名、原帖用户id、原帖用户名、原帖url的域名）
# 修改1：在retweet_expanded_urls_array和quoted_expanded_urls_array去media_url_domain里匹配之前需要将这两个字段里的url提取出域名出来
# 修改2：把匹配上的domain也保存在新文件里
def process_month(directory, media_url_domain):
    # 读取所有输出文件
    output_files = glob(os.path.join(directory, '****-**-**-*-output.csv'))

    # 初始化一个空的 DataFrame 用于存储匹配的转发信息
    matching_media_df = pd.DataFrame()

    # 处理每个输出文件
    for file in output_files:
        print(f'正在处理{file}')
        df = pd.read_csv(file, dtype=str)

        # 提取 retweet_expanded_urls_array 和 quoted_expanded_urls_array 字段的域名
        df['retweet_domain'] = df['retweet_expanded_urls_array'].apply(
            lambda x: extract_domain(x) if pd.notna(x) else None)
        df['quote_domain'] = df['quoted_expanded_urls_array'].apply(
            lambda x: extract_domain(x) if pd.notna(x) else None)

        # 使用矢量化操作来筛选retweet_domain和quote_domain
        retweet_match = df['retweet_domain'].isin(media_url_domain)
        quote_match = df['quote_domain'].isin(media_url_domain)

        # 创建一个新的DataFrame，只保留符合条件的行
        matching_retweets = df[retweet_match | quote_match].copy()

        # 如果是quoted_expanded_urls_array匹配，则替换对应的retweet_origin_user_id和retweet_origin_username
        matching_retweets.loc[quote_match, 'retweet_origin_user_id'] = matching_retweets['quoted_origin_user_id']
        matching_retweets.loc[quote_match, 'retweet_origin_username'] = matching_retweets['quoted_origin_username']
        # 添加匹配到的域名到新的列
        matching_retweets['matched_domain'] = matching_retweets.apply(
            lambda row: row['retweet_domain'] if row['retweet_domain'] in media_url_domain else row['quote_domain'],
            axis=1
        )
        # 只保留所需的列
        matching_retweets = matching_retweets[
            ['retweeted_user_id', 'retweeted_username', 'retweet_origin_user_id', 'retweet_origin_username', 'matched_domain']]

        # 追加到结果 DataFrame
        matching_media_df = pd.concat([matching_media_df, matching_retweets], ignore_index=True)

        # 保存结果到新的 CSV 文件
    name = os.path.join('F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Media', directory.split('\\')[-1])
    print(name)
    matching_media_df.to_csv(f'{name}.csv', index=False)
    print(f"已成功筛选并保存媒体的转发信息到{name}")







def main():
    # 读取包含政客账号信息的 CSV 文件
    directory = r'F:\us-presidential-output'
    # directory = r'F:\three_parts_output\test'# 先测试

    # 媒体域名标签文件，表头只有：domain,bias
    combined_df = pd.read_csv(r'F:\Experimental Results\media-bias-final-url-cleaned.csv', dtype=str)
    political_leanings_df = combined_df.dropna(subset=['bias'])
    media_url_domain = set(political_leanings_df['domain'])
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
            process_month(folder_path, media_url_domain)


main()

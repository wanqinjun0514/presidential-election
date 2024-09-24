import os
import pandas as pd
from glob import glob
import re
from openpyxl import load_workbook

# 这版代码没有考虑到三个部分数据的转发关系不同
# 请帮我修改以下代码，把directory部分改成读取三个文件夹下的以-output.csv结尾的csv文件，三个部分的数据依次是：F:\three_parts_output\without_url、F:\three_parts_output\single_url\external_url、F:\three_parts_output\single_url\twitter_url
# 这三个部分的数据提取出转发关系的方式稍微有一些不同，without_url部分是匹配politician_user_ids没问题，保留四列数据（转发用户id、转发用户名、原帖用户id、原帖用户名），这里的原帖用户id就是唯一标识政客的id了，可以直接输入到奇异值矩阵分解部分进行分解打分
def process_month_without_url(directory, politician_user_ids):
    # 读取所有输出文件
    output_files = glob(os.path.join(directory, '2019-12-01-1-output.csv'))
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
    name = os.path.join('F:\code\WQJ\平均值被打上分的推文数量和矩阵分解之前的简化转发关系数量对不上', directory.split('\\')[-1])
    print(name)
    matching_politician_df.to_csv(f'{name}.csv', index=False)
    print(f"已成功筛选并保存政客的转发信息到{name}")


# 以下是在整理政客标签
def 原来的政客标签没有清洗_有标签的和没有bias标签的都放在一起了很乱_单独整理出来():
    combined_df = pd.read_csv(
        r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\combined_with_screenname_and_bias.csv',
        dtype=str)
    politician_df = combined_df.dropna(subset=['bias'])
    # 删除 retweet_origin_user_id 重复的数据，只保留第一条
    politician_df_cleaned = politician_df.drop_duplicates(subset=['retweet_origin_user_id'], keep='first')
    results_file = rf'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\政客标签_去重之后_final.csv'
    politician_df_cleaned.to_csv(results_file, index=False, columns=['retweet_origin_user_id', 'bias', 'retweet_origin_username', 'screen_name'])

def 找到政客标签里重复数据():
    # 读取CSV文件
    combined_df = pd.read_csv(
        r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\combined_with_screenname_and_bias.csv',
        dtype=str)

    # 过滤掉没有 bias 的数据
    politician_df = combined_df.dropna(subset=['bias'])

    # 找到 retweet_origin_user_id 出现次数超过1次的数据
    # 找有没有同名的政客
    multiple_occurrences = politician_df.groupby('retweet_origin_username').filter(lambda x: len(x) > 1)

    # 输出结果到新的CSV文件
    results_file = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\政客标签_重复数据_final.csv'
    multiple_occurrences.to_csv(results_file, index=False, columns=['retweet_origin_username', 'bias'])
    # 打印筛选出的结果（可选）
    print(multiple_occurrences)


# 构建词表这块的内容，我要检查有哪些推文是重复的（之前去重的数据和我现在去重的结果都不太一样，一个月的数据差几十个吧）
def 找到去重之后还有没有重复的推文数据():
    df = pd.read_csv(
        r'F:\Intermediate Results\original_fulltext_and_tweet_id_spacy_drop_duplicate\combined_original_fulltext_and_tweet_id_2019_12_with_languages.csv',
        dtype=str)
    multiple_occurrences = df.groupby('retweet_id').filter(lambda x: len(x) > 1)
    print(multiple_occurrences)




# 终于调对啦！！！！！！！！！！！！！！！！！！
def 由于矩阵分解的简化转发关系数据和平均值的打分政客影响用户的关系数量对不上所以再检查一下(politician_user_ids):
    # 读取所有输出文件
    # months = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
    #           '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']
    months = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
              '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']
    for month in months:
        directory = rf'F:\three_parts_output\without_url\output_{month}'
        # directory = rf'F:\code\WQJ\平均值被打上分的推文数量和矩阵分解之前的简化转发关系数量对不上_终于改对啦\test'

        output_files = glob(os.path.join(directory, '****-**-**-*-output.csv'))
        results_file = rf'F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Politician_new\矩阵分解简化转发关系_{month}.csv'
        # 保存详细转发数据到 Excel
        statistic_results_file = rf'F:\Intermediate Results\Simplyfied Forwarding relationship\矩阵分解简化转发关系统计_{month}.csv'
        total_retweet_count = 0
        total_quote_count = 0
        summary_data = []
        result_data = []
        # 处理每个输出文件
        for file in output_files:
            print(f'正在处理{file}')
            df = pd.read_csv(file, dtype=str)
            # retweeted_user_id是output里的第3列
            # retweeted_username是output里的第4列
            # retweet_origin_user_id是output里的第10列
            # retweet_origin_username是output里的第11列
            # quoted_origin_user_id是output里的第20列
            # quoted_origin_username是output里的第21列
            retweet_count = 0
            quote_count = 0
            if len(df.columns) >= 21:
                # Loop through each row
                for index, row in df.iterrows():
                    # Check if the row has enough columns
                    if len(row) >= 21:
                        retweeted_user_id = row.iloc[2]  # 3rd column
                        retweeted_username = row.iloc[3]
                        retweet_origin_user_id = row.iloc[9]  # 10th column
                        retweet_origin_username = row.iloc[10]
                        quote_origin_user_id = row.iloc[19]  # 20th column
                        quoted_origin_username = row.iloc[20]
                        # Check if either 10th or 20th column is in the value_map
                        if (retweet_origin_user_id in politician_user_ids) or (quote_origin_user_id in politician_user_ids):
                            # Determine which one is not empty for retweet_or_quote_origin_user_id
                            retweet_or_quote_origin_user_id = retweet_origin_user_id if pd.notna(retweet_origin_user_id) else quote_origin_user_id
                            retweet_or_quote_origin_username = retweet_origin_username if pd.notna(retweet_origin_username) else quoted_origin_username
                            # Increment retweet or quote count
                            if retweet_origin_user_id in politician_user_ids:  # 如果在字典里
                                retweet_count += 1
                            if quote_origin_user_id in politician_user_ids:
                                quote_count += 1
                            # Append to result list
                            result_data.append({
                                'retweeted_user_id': retweeted_user_id,
                                'retweeted_username': retweeted_username,
                                'retweet_or_quote_origin_user_id': retweet_or_quote_origin_user_id,
                                'retweet_or_quote_origin_username': retweet_or_quote_origin_username
                            })
            else:
                print(f"Skipping file {file} because it doesn't have enough columns.")
            # Print the retweet and quote counts
            print(f"文件 {file}里能被政客标签影响的总的转贴次数为: {retweet_count}")
            print(f"文件 {file}的被政客标签影响的总的引用帖子次数为 {quote_count}")
            retweet_and_quote_count = retweet_count + quote_count
            print(f"文件 {file}的被政客标签影响的总的转贴和引用帖子次数为 {retweet_and_quote_count}")
            total_retweet_count += retweet_count
            total_quote_count += quote_count
            # 将每个文件的结果存入 summary_data 列表
            summary_data.append({
                '文件名': file,
                '转发次数': retweet_count,
                '引用次数': quote_count,
                '转贴和引用次数': retweet_and_quote_count
            })
        print(f"{directory}路径下的所有文件里能被政客标签影响的总的转贴次数为: {total_retweet_count}")
        print(f"{directory}路径下的所有文件里被政客标签影响的总的引用帖子次数为 {total_quote_count}")
        total_count = total_retweet_count + total_quote_count
        print(f"{directory}路径下的所有文件里被政客标签影响的总的转贴和引用帖子次数为 {total_count}")
        statistic_results_df = pd.DataFrame(summary_data)
        statistic_results_df.to_csv(statistic_results_file, index=False)
        print(f"已成功筛选并保存政客的转发信息和统计数据到 {statistic_results_file}")

        result_df = pd.DataFrame(result_data)
        result_df.to_csv(results_file, index=False, columns=['retweeted_user_id', 'retweeted_username', 'retweet_or_quote_origin_user_id', 'retweet_or_quote_origin_username'])
        print(f"已成功筛选并保存政客的转发信息到{results_file}")

def process_without_url_fowarding_relationship_main():
    combined_df = pd.read_csv(r'F:\code\政客标签_去重之后_final.csv',dtype=str)
    politician_user_ids = set(combined_df['retweet_origin_user_id'])# 这里不应该写成dict,注意 combined_df['retweet_origin_user_id'] 返回的是一个 Series，而不是字典。如果你想创建一个字典，可能需要调整为：set
    print(f'{len(politician_user_ids)}')
    print(politician_user_ids)
    由于矩阵分解的简化转发关系数据和平均值的打分政客影响用户的关系数量对不上所以再检查一下(politician_user_ids)



# 提取用户名函数
def extract_username(url):
    match = re.search(r"https://twitter.com/([^/]+)/", url)
    if match:
        return match.group(1)
    return None

# twitter_url部分是要提取出twitter.com后面的username再和政客标签里的politician_user_ids进行匹配，保留6列数据（转发用户id、转发用户名、原帖用户id、原帖用户名、匹配的政客username、政客的id-这个字段是从标签文件里获取的）
def process_month_twitter_url_old_直接对dataframe进行操作的我怕出错(politician_username):
    directory =rf'F:\three_parts_output\single_url\twitter_url\output_2019_12'
    # 读取所有输出文件
    # output_files = glob(os.path.join(directory, '****-**-**-*-output.csv'))

    output_files = glob(os.path.join(directory, '2019-12-01-1-output.csv'))

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
        # 将 retweet_match 或 quote_match 为 True 的行筛选出来，生成新的 DataFrame matching_retweets，即只保留那些转发或引用了政客推文的行
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
    name = os.path.join(r'F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Politician_new', directory.split('\\')[-1])
    print(name)
    matching_politician_df.to_csv(f'{name}.csv', index=False)
    print(f"已成功筛选并保存政客的转发信息到{name}")


# 这个是对的！！！！！！！！！！！！！！
def process_month_twitter_url(politician_username):
    months = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
              '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']
    for month in months:
        directory = rf'F:\three_parts_output\single_url\twitter_url\output_{month}'
        output_files = glob(os.path.join(directory, '*-output.csv'))
        statistic_results_file = rf'F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Politician\twitter_url\矩阵分解方法的之前的简化转发关系统计_{month}.csv'
        output_folder = rf'F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Politician\twitter_url'
        # 初始化一个空的 DataFrame 用于存储匹配的转发信息
        matching_politician_df = pd.DataFrame()
        result_data = []
        total_retweet_count = 0
        total_quote_count = 0
        summary_data = []
        # 处理每个输出文件
        for file in output_files:
            print(f'正在处理{file}')
            df = pd.read_csv(file, dtype=str)
            retweet_count = 0
            quote_count = 0
            # 初始化存储匹配结果的列表
            retweeted_user_id_list = []
            retweeted_username_list = []
            retweet_origin_user_id_list = []
            retweet_origin_username_list = []
            retweet_origin_screenname_list = []

            # 逐行处理 DataFrame
            for index, row in df.iterrows():
                # 提取 retweet_expanded_urls_array 和 quoted_expanded_urls_array 中的用户名
                retweet_username = extract_username(row['retweet_expanded_urls_array']) if pd.notna(row['retweet_expanded_urls_array']) else None
                quote_username = extract_username(row['quoted_expanded_urls_array']) if pd.notna(row['quoted_expanded_urls_array']) else None

                # 初始化 retweet_origin_screenname 为 None
                retweet_origin_screenname = None
                retweet_origin_user_id = row['retweet_origin_user_id']
                retweet_origin_username = row['retweet_origin_username']

                # 匹配政客的用户名
                if retweet_username in politician_username:
                    # 如果匹配的是转发的用户名
                    retweet_origin_screenname = retweet_username
                    retweet_count += 1
                elif quote_username in politician_username:
                    # 如果匹配的是引用的用户名，替换为引用信息
                    retweet_origin_screenname = quote_username
                    retweet_origin_user_id = row['quoted_origin_user_id']
                    retweet_origin_username = row['quoted_origin_username']
                    quote_count += 1

                # 如果匹配到政客的用户名，记录结果
                if retweet_origin_screenname:
                    retweeted_user_id_list.append(row['retweeted_user_id'])
                    retweeted_username_list.append(row['retweeted_username'])
                    retweet_origin_user_id_list.append(retweet_origin_user_id)
                    retweet_origin_username_list.append(retweet_origin_username)
                    retweet_origin_screenname_list.append(retweet_origin_screenname)
            print(f"文件 {file}里能被政客标签影响的总的转贴次数为: {retweet_count}")
            print(f"文件 {file}的被政客标签影响的总的引用帖子次数为 {quote_count}")
            retweet_and_quote_count = retweet_count + quote_count
            print(f"文件 {file}的被政客标签影响的总的转贴和引用帖子次数为 {retweet_and_quote_count}")
            total_retweet_count += retweet_count
            total_quote_count += quote_count
            # 将每个文件的结果存入 summary_data 列表
            summary_data.append({
                '文件名': file,
                '转发次数': retweet_count,
                '引用次数': quote_count,
                '转贴和引用次数': retweet_and_quote_count
            })
            # 将匹配到的结果追加到 DataFrame 中
            temp_df = pd.DataFrame({
                'retweeted_user_id': retweeted_user_id_list,
                'retweeted_username': retweeted_username_list,
                'retweet_origin_user_id': retweet_origin_user_id_list,
                'retweet_origin_username': retweet_origin_username_list,
                'retweet_origin_screenname': retweet_origin_screenname_list
            })
            matching_politician_df = pd.concat([matching_politician_df, temp_df], ignore_index=True)

        # 保存结果到新的 CSV 文件

        output_file_path = os.path.join(output_folder, rf'politician_influence_Simplyfied_Forwarding_output_{month}.csv')
        print(output_file_path)
        matching_politician_df.to_csv(output_file_path, index=False)
        print(f"已成功筛选并保存政客的转发信息到{output_file_path}")
        print(f"{directory}路径下的所有文件里能被政客标签影响的总的转贴次数为: {total_retweet_count}")
        print(f"{directory}路径下的所有文件里被政客标签影响的总的引用帖子次数为 {total_quote_count}")
        total_count = total_retweet_count + total_quote_count
        print(f"{directory}路径下的所有文件里被政客标签影响的总的转贴和引用帖子次数为 {total_count}")
        statistic_results_df = pd.DataFrame(summary_data)
        statistic_results_df.to_csv(statistic_results_file, index=False)
        print(f"已成功筛选并保存政客的转发信息和统计数据到 {statistic_results_file}")



def process_twitter_url_fowarding_relationship_main():
    # 读取包含政客账号信息的 CSV 文件
    combined_df = pd.read_csv(
        r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\政客标签_去重之后_final.csv',
        dtype=str)
    politician_df = combined_df.dropna(subset=['bias'])
    politician_username = set(politician_df['screen_name'])#这里匹配twitter_url后面的数据需要将原帖用户id改成screenname
    process_month_twitter_url(politician_username)

# 提取Domain函数
def extract_domain(url):
    # 处理带有协议的URL（http 或 https），提取主域名
    match = re.search(r"https?://(?:www\.)?([^/]+)", url)
    if match:
        return match.group(1)
    return None

def process_month_external_url_直接对dataframe进行操作的我怕出错(directory, politician_domain):
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


def process_month_external_url(politician_username):
    # months = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
    #           '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']
    # for month in months:
    month = '2019_12'
    directory = rf'F:\three_parts_output\single_url\twitter_url\output_{month}'
    output_files = glob(os.path.join(directory, '*-output.csv'))
    statistic_results_file = rf'F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Politician\twitter_url\矩阵分解方法的之前的简化转发关系统计_{month}.csv'
    output_folder = rf'F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Politician\twitter_url'
    # 初始化一个空的 DataFrame 用于存储匹配的转发信息
    matching_politician_df = pd.DataFrame()
    result_data = []
    total_retweet_count = 0
    total_quote_count = 0
    summary_data = []
    # 处理每个输出文件
    for file in output_files:
        print(f'正在处理{file}')
        df = pd.read_csv(file, dtype=str)
        retweet_count = 0
        quote_count = 0
        # 初始化存储匹配结果的列表
        retweeted_user_id_list = []
        retweeted_username_list = []
        retweet_origin_user_id_list = []
        retweet_origin_username_list = []
        retweet_origin_screenname_list = []

        # 逐行处理 DataFrame
        for index, row in df.iterrows():
            # 提取 retweet_expanded_urls_array 和 quoted_expanded_urls_array 中的用户名
            retweet_username = extract_username(row['retweet_expanded_urls_array']) if pd.notna(
                row['retweet_expanded_urls_array']) else None
            quote_username = extract_username(row['quoted_expanded_urls_array']) if pd.notna(
                row['quoted_expanded_urls_array']) else None

            # 初始化 retweet_origin_screenname 为 None
            retweet_origin_screenname = None
            retweet_origin_user_id = row['retweet_origin_user_id']
            retweet_origin_username = row['retweet_origin_username']

            # 匹配政客的用户名
            if retweet_username in politician_username:
                # 如果匹配的是转发的用户名
                retweet_origin_screenname = retweet_username
                retweet_count += 1
            elif quote_username in politician_username:
                # 如果匹配的是引用的用户名，替换为引用信息
                retweet_origin_screenname = quote_username
                retweet_origin_user_id = row['quoted_origin_user_id']
                retweet_origin_username = row['quoted_origin_username']
                quote_count += 1

            # 如果匹配到政客的用户名，记录结果
            if retweet_origin_screenname:
                retweeted_user_id_list.append(row['retweeted_user_id'])
                retweeted_username_list.append(row['retweeted_username'])
                retweet_origin_user_id_list.append(retweet_origin_user_id)
                retweet_origin_username_list.append(retweet_origin_username)
                retweet_origin_screenname_list.append(retweet_origin_screenname)
        print(f"文件 {file}里能被政客标签影响的总的转贴次数为: {retweet_count}")
        print(f"文件 {file}的被政客标签影响的总的引用帖子次数为 {quote_count}")
        retweet_and_quote_count = retweet_count + quote_count
        print(f"文件 {file}的被政客标签影响的总的转贴和引用帖子次数为 {retweet_and_quote_count}")
        total_retweet_count += retweet_count
        total_quote_count += quote_count
        # 将每个文件的结果存入 summary_data 列表
        summary_data.append({
            '文件名': file,
            '转发次数': retweet_count,
            '引用次数': quote_count,
            '转贴和引用次数': retweet_and_quote_count
        })
        # 将匹配到的结果追加到 DataFrame 中
        temp_df = pd.DataFrame({
            'retweeted_user_id': retweeted_user_id_list,
            'retweeted_username': retweeted_username_list,
            'retweet_origin_user_id': retweet_origin_user_id_list,
            'retweet_origin_username': retweet_origin_username_list,
            'retweet_origin_screenname': retweet_origin_screenname_list
        })
        matching_politician_df = pd.concat([matching_politician_df, temp_df], ignore_index=True)

    # 保存结果到新的 CSV 文件

    output_file_path = os.path.join(output_folder, rf'politician_influence_Simplyfied_Forwarding_output_{month}.csv')
    print(output_file_path)
    matching_politician_df.to_csv(output_file_path, index=False)
    print(f"已成功筛选并保存政客的转发信息到{output_file_path}")
    print(f"{directory}路径下的所有文件里能被政客标签影响的总的转贴次数为: {total_retweet_count}")
    print(f"{directory}路径下的所有文件里被政客标签影响的总的引用帖子次数为 {total_quote_count}")
    total_count = total_retweet_count + total_quote_count
    print(f"{directory}路径下的所有文件里被政客标签影响的总的转贴和引用帖子次数为 {total_count}")
    statistic_results_df = pd.DataFrame(summary_data)
    statistic_results_df.to_csv(statistic_results_file, index=False)
    print(f"已成功筛选并保存政客的转发信息和统计数据到 {statistic_results_file}")






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


# 由于平均值和矩阵分解简化转发关系的数据始终对不上，把平均值的方法按照逻辑都改好了，再把矩阵分解这块改成了按行处理，结果还是对不上，所以直接找两个测试结果文件的推文id不同在哪




if __name__ == '__main__':
    # 原来的政客标签没有清洗_有标签的和没有bias标签的都放在一起了很乱_单独整理出来()
    # 找到政客标签里重复数据()
    # process_without_url_fowarding_relationship_main()
    process_twitter_url_fowarding_relationship_main()
    # process_external_url_fowarding_relationship_main()

    # 找到去重之后还有没有重复的推文数据()

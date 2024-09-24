import pandas as pd
import os
import re

def get_bias_dict():
    # external_url部分数据的标签文件
    file_path = rf'F:\Experimental Results\Average_Bias_Rating\politician_url_bias.csv'
    # 读取CSV文件
    df = pd.read_csv(file_path, dtype={0: str, 4: str})
    # 提取第1列和第5列
    first_column = df.iloc[:, 0]
    fifth_column = df.iloc[:, 4]
    # 转换第5列中的字符串
    fifth_column = fifth_column.map({'Left': -1, 'Right': 1, 'Center': 0}).dropna()
    # 创建映射字典
    mapping_dict = dict(zip(first_column, fifth_column))
    return mapping_dict

# 提取Domain函数
def extract_domain(url):
    # 处理带有协议的URL（http 或 https），提取主域名
    match = re.search(r"https?://(?:www\.)?([^/]+)", url)
    if match:
        return match.group(1)
    return None



def 在完整external_url里提取出每个月的政客能影响的用户_给用户打分的第一步(value_map):
    months = [
        '2019_12',
              '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
              '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']
    for month in months:
        # Example usage
        input_folder = rf'F:\three_parts_output\single_url\external_url\output_{month}'
        # input_folder = r'F:\code\WQJ\平均值被打上分的推文数量和矩阵分解之前的简化转发关系数量对不上_终于改对啦\test'#测试
        output_folder = rf'F:\Intermediate Results\Average_Bias_Rating\external_url_politician_influence_output'  # 测试
        # 保存详细转发数据到 Excel
        statistic_results_file = rf'F:\Intermediate Results\Average_Bias_Rating\external_url_politician_influence_output\平均值方法的简化转发关系统计_{month}.csv'

        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Prepare output file path
        output_file_path = os.path.join(output_folder, rf'politician_influence_output_{month}.csv')

        # Prepare the list to store the extracted rows
        result_data = []
        total_retweet_count = 0
        total_quote_count = 0
        summary_data = []
        # Loop through all files in the input folder
        for file_name in os.listdir(input_folder):
            if file_name.endswith('-output.csv'):
                file_path = os.path.join(input_folder, file_name)
                # Read the csv file
                df = pd.read_csv(file_path, dtype=str)
                print('正在读取文件:', file_path)
                retweet_count = 0
                quote_count = 0
                if len(df.columns) >= 20:
                    # Loop through each row
                    for index, row in df.iterrows():
                        # Check if the row has enough columns
                        if len(row) >= 20:
                            retweeted_user_id = row.iloc[2]  # 3rd column
                            retweet_expanded_urls_array = row.iloc[8]  # 9th column
                            retweet_origin_user_id = row.iloc[9]  # 10th column
                            quoted_expanded_urls_array = row.iloc[18]  # 19th column
                            quote_origin_user_id = row.iloc[19]  # 20th column
                            # 检查twitter.com后面的用户名之后，这个用户名是否在构建的政客字典里，在的话就算政客标签被转发或者引用，成功影响到了用户
                            match_retweet_expanded_urls_username = extract_domain(str(retweet_expanded_urls_array))
                            match_quoted_expanded_urls_username = extract_domain(str(quoted_expanded_urls_array))
                            # twitter这部分要简化的转发关系里要保存的数据是：当前帖子的用户id、原帖的用户id、twitter.com后面匹配到的政客用户名、该政客的bias分数
                            # Check if either 10th or 20th column is in the value_map
                            if (match_retweet_expanded_urls_username in value_map) or (
                                    match_quoted_expanded_urls_username in value_map):
                                # Determine which one is not empty for retweet_or_quote_origin_user_id
                                # 确定原帖的用户id
                                retweet_or_quote_origin_user_id = retweet_origin_user_id if pd.notna(
                                    retweet_origin_user_id) else quote_origin_user_id
                                # 确定twitter.com后面匹配到的政客用户名
                                match_retweet_or_quote_username = match_retweet_expanded_urls_username if pd.notna(
                                    match_retweet_expanded_urls_username) else match_quoted_expanded_urls_username
                                bias_value = value_map[match_retweet_or_quote_username]

                                # Increment retweet or quote count
                                if match_retweet_expanded_urls_username in value_map:  # 如果在字典里
                                    retweet_count += 1
                                if match_quoted_expanded_urls_username in value_map:
                                    quote_count += 1
                                # Append to result list
                                result_data.append({
                                    'retweeted_user_id': retweeted_user_id,
                                    'retweet_or_quote_origin_user_id': retweet_or_quote_origin_user_id,
                                    'match_retweet_or_quote_username': match_retweet_or_quote_username,
                                    'bias_value': bias_value
                                })
                else:
                    print(f"Skipping file {file_name} because it doesn't have enough columns.")
                # Print the retweet and quote counts
                print(f"文件 {file_path}里能被政客标签影响的总的转贴次数为: {retweet_count}")
                print(f"文件 {file_path}的被政客标签影响的总的引用帖子次数为 {quote_count}")
                retweet_and_quote_count = retweet_count + quote_count
                print(f"文件 {file_path}的被政客标签影响的总的转贴和引用帖子次数为 {retweet_and_quote_count}")
                total_retweet_count += retweet_count
                total_quote_count += quote_count
                # 将每个文件的结果存入 summary_data 列表
                summary_data.append({
                    '文件名': file_path,
                    '转发次数': retweet_count,
                    '引用次数': quote_count,
                    '转贴和引用次数': retweet_and_quote_count
                })
        print(f"{input_folder}路径下的所有文件里能被政客标签影响的总的转贴次数为: {total_retweet_count}")
        print(f"{input_folder}路径下的所有文件里被政客标签影响的总的引用帖子次数为 {total_quote_count}")
        total_count = total_retweet_count + total_quote_count
        print(f"{input_folder}路径下的所有文件里被政客标签影响的总的转贴和引用帖子次数为 {total_count}")
        statistic_results_df = pd.DataFrame(summary_data)
        statistic_results_df.to_csv(statistic_results_file, index=False)
        print(f"已成功筛选并保存政客的转发信息和统计数据到 {statistic_results_file}")
        # Convert the result list to a DataFrame and save as CSV
        if result_data:
            result_df = pd.DataFrame(result_data)
            result_df.to_csv(output_file_path, index=False, columns=['retweeted_user_id', 'retweet_or_quote_origin_user_id',
                                                                     'match_retweet_or_quote_username', 'bias_value'])


if __name__ == '__main__':
    bias_dict = get_bias_dict()
    在完整external_url里提取出每个月的政客能影响的用户_给用户打分的第一步(bias_dict)



import pandas as pd
import os
from tqdm import tqdm

def get_bias_dict():
    # 以前的政客标签文件路径
    # file_path = rf'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\combined_with_screenname_and_bias.csv'
    file_path = r'F:\code\政客标签_去重之后_final.csv'
    # 读取CSV文件
    df = pd.read_csv(file_path, dtype={0: str, 1: str})
    # 提取第1列和第5列
    first_column = df.iloc[:, 0]
    fifth_column = df.iloc[:, 1]
    # 转换第5列中的字符串
    fifth_column = fifth_column.map({'Left': -1, 'Right': 1, 'Center': 0}).dropna()
    # 创建映射字典
    mapping_dict = dict(zip(first_column, fifth_column))
    return mapping_dict


# 专门处理without_url部分数据的打分
# 把打分的流程拆分一下，还是不要一次做到位，很可能出错
# 帮我写一个函数，处理文件夹F:\three_parts_output\without_url\output_2019_12下所有的以-output.csv结尾的csv文件，读取所有的csv文件的提取第3列、第10列、第20列，如果第10列、第20列在value_map的字典里（value_map字典是id到一个分数的映射关系），如果第10列、第20列在value_map的字典至少有一列的值在字典中存在
# 那就把第3列、第10列、第20列的数据保存在新的csv里，第三列肯定不为空，可以保存在新文件的retweeted_user_id字段，第10列、第20列我确定所有数据里这两列数据最多只有一个数据是不为空，不存在第10列和第20列都不为空的情况，就将不为空的那个数据保存在新文件的retweet_or_quote_origin_user_id字段里，新文件的表头可以是retweeted_user_id，retweet_or_quote_origin_user_id这两列,文件保存在F:\Intermediate Results\Average_Bias_Rating\politician_influence_output_2019_12
def 在完整without_url里提取出每个月的政客能影响的用户_给用户打分的第一步(value_map):
    months = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
              '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']
    for month in months:
        # Example usage
        input_folder = rf'F:\three_parts_output\without_url\output_{month}'
        # input_folder = r'F:\code\WQJ\平均值被打上分的推文数量和矩阵分解之前的简化转发关系数量对不上_终于改对啦\test'#测试
        output_folder = rf'F:\Intermediate Results\Average_Bias_Rating\politician_influence_output'#测试
        # 保存详细转发数据到 Excel
        statistic_results_file = rf'F:\Intermediate Results\Average_Bias_Rating\politician_influence_output\平均值方法的简化转发关系统计_{month}.csv'

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
                            retweet_origin_user_id = row.iloc[9]  # 10th column
                            quote_origin_user_id = row.iloc[19]  # 20th column

                            # Check if either 10th or 20th column is in the value_map
                            if (retweet_origin_user_id in value_map) or (quote_origin_user_id in value_map):
                                # Determine which one is not empty for retweet_or_quote_origin_user_id
                                retweet_or_quote_origin_user_id = retweet_origin_user_id if pd.notna(retweet_origin_user_id) else quote_origin_user_id
                                bias_value = value_map[retweet_or_quote_origin_user_id]
                                # Increment retweet or quote count
                                if retweet_origin_user_id in value_map:# 如果在字典里
                                    retweet_count += 1
                                if quote_origin_user_id in value_map:
                                    quote_count += 1
                                # Append to result list
                                result_data.append({
                                    'retweeted_user_id': retweeted_user_id,
                                    'retweet_or_quote_origin_user_id': retweet_or_quote_origin_user_id,
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
            result_df.to_csv(output_file_path, index=False, columns=['retweeted_user_id', 'retweet_or_quote_origin_user_id', 'bias_value'])

# 把匹配上id的分数累加到第三列的用户id上，需要建立2个空的字典，第一个字典里面保存retweeted_user_id，映射到每个用户id对应的bias_value列的总分数（retweeted_user_id可能出现多次，在不同的行里retweeted_user_id对应的bias_value值可能不一样，把每个相同的retweeted_user_id对应的所有bias_value值累加起来），第二个字典里保存retweeted_user_id，以及这个用户id在文件中的retweeted_user_id列里出现的总次数
# 把两个字典按照用户id对应保存在一个新的csv文件里，新csv的表头是retweeted_user_id、total_bias_points、retweet_times、average_bias_points一共四列，最后一列是用每一行的total_bias_points除以retweet_times得到average_bias_points
def 根据平均值第一步里简化的转发关系的结果计算每个月的每个用户的总bias分数和次数以及政治倾向平均值():
    months = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
              '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']
    for month in months:
        # 文件路径
        file_path = rf'F:\Intermediate Results\Average_Bias_Rating\external_url_politician_influence_output\politician_influence_output_{month}.csv'
        # 读取 CSV 文件
        df = pd.read_csv(file_path,
                         dtype={'retweeted_user_id': str, 'retweet_or_quote_origin_user_id': str, 'bias_value': float})
        print('正在处理文件：', file_path)
        # 初始化两个字典
        total_bias_points_dict = {}
        retweet_times_dict = {}
        # 遍历 DataFrame 的每一行
        for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing rows"):
            retweeted_user_id = row['retweeted_user_id']
            bias_value = row['bias_value']
            # 累加 bias_value 到 total_bias_points_dict
            if retweeted_user_id in total_bias_points_dict:
                total_bias_points_dict[retweeted_user_id] += bias_value
            else:
                total_bias_points_dict[retweeted_user_id] = bias_value
            # 统计 retweeted_user_id 出现的次数
            if retweeted_user_id in retweet_times_dict:
                retweet_times_dict[retweeted_user_id] += 1
            else:
                retweet_times_dict[retweeted_user_id] = 1


        # 计算 retweet_times_dict 中次数的总和
        total_retweet_times = sum(retweet_times_dict.values())
        print(f"Retweet times total: {total_retweet_times}")
        # 构建新的 DataFrame 来保存最终的结果
        result_data = []
        for retweeted_user_id in total_bias_points_dict:
            total_bias_points = total_bias_points_dict[retweeted_user_id]
            retweet_times = retweet_times_dict[retweeted_user_id]
            average_bias_points = total_bias_points / retweet_times  # 计算平均 bias 值
            result_data.append({
                'retweeted_user_id': retweeted_user_id,
                'total_bias_points': total_bias_points,
                'retweet_times': retweet_times,
                'average_bias_points': average_bias_points
            })
        result_df = pd.DataFrame(result_data)
        # 输出到新的 CSV 文件
        output_file = rf'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\external_url-rating\monthly_users_bias\{month}_output.csv'
        result_df.to_csv(output_file, index=False)
        print(f"处理结果已保存到 {output_file}")


if __name__ == '__main__':
    # bias_dict = get_bias_dict()# 将原帖用户id转换成bias分数
    # 在完整without_url里提取出每个月的政客能影响的用户_给用户打分的第一步(bias_dict)
    根据平均值第一步里简化的转发关系的结果计算每个月的每个用户的总bias分数和次数以及政治倾向平均值()

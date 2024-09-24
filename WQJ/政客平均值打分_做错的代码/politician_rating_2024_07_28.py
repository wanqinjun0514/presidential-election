import pandas as pd
import os


def get_bias_dict(file_path):
    # 读取CSV文件
    df = pd.read_csv(file_path, dtype= str)

    # 提取第1列和第5列
    first_column = df.iloc[:, 0]
    fifth_column = df.iloc[:, 4]

    # 转换第5列中的字符串
    fifth_column = fifth_column.map({'Left': -1, 'Right': 1, 'Center': 0}).dropna()

    # 创建映射字典
    mapping_dict = dict(zip(first_column, fifth_column))

    return mapping_dict


def process_folder(folder_path, value_map, output_file_path):
    # 初始化一个空的DataFrame来存储结果
    result_df = pd.DataFrame(columns=['retweeted_user_id', 'total_bias_points', 'retweet_times', 'average_bias_points'])

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)

            # 读取CSV文件，确保第3列和第10列为字符串类型
            df = pd.read_csv(file_path, dtype= str)

            # 提取第10列和第3列
            tenth_column = df.iloc[:, 9]  # 第10列的索引为9
            third_column = df.iloc[:, 2]  # 第3列的索引为2

            # 将第十列的值根据映射字典转换
            mapped_values = tenth_column.map(value_map).fillna(0)  # 将NaN替换为0

            # 确保第十列的值在字典中存在
            valid_mask = mapped_values != 0
            valid_third_column = third_column[valid_mask]
            valid_mapped_values = mapped_values[valid_mask]

            # 合并第三列和转换后的第十列
            merged_data = pd.concat([valid_third_column, valid_mapped_values], axis=1)
            merged_data.columns = ['retweeted_user_id', 'mapped_value']

            # 按retweeted_user_id分组并计算总和、计数和平均值
            grouped_data = merged_data.groupby('retweeted_user_id').agg(
                total_bias_points=('mapped_value', 'sum'),
                retweet_times=('mapped_value', 'size'),
                average_bias_points=('mapped_value', 'mean')
            ).reset_index()

            # 将结果添加到总的DataFrame中
            result_df = pd.concat([result_df, grouped_data])

    # 输出结果到新的CSV文件
    result_df.to_csv(output_file_path, index=False)
    print(f"Results saved to {output_file_path}")



# 使用文件路径调用函数
file_path = rf'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\combined_with_screenname_and_bias.csv'
bias_dict = get_bias_dict(file_path)


# start_year = 2019
# start_month = 12
start_year = 2021
start_month = 2
end_year = 2021
end_month = 2


base_folder_path = rf'F:\three_parts_output\without_url'
output_base_folder_path = rf'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\2_monthly_users_bias'
for year in range(start_year, end_year + 1):
    for month in range(start_month if year == start_year else 1, end_month + 1 if year == end_year else 13):
        folder_name=f"output_{year}_{month:02d}"
        folder_path=os.path.join(base_folder_path, folder_name)
        output_file_name = f"{year}_{month:02d}_output.csv"
        output_file_path = os.path.join(output_base_folder_path, output_file_name)

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            print(f"Processing folder: {folder_name}")
            process_folder(folder_path, bias_dict, output_file_path)
        else:
            print(f"Folder not found:{folder_name}")



import pandas as pd
import glob
import os

# 定义你的CSV文件路径和组别信息
csv_files = sorted(glob.glob(rf'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\2_monthly_users_bias\*_output.csv'))  # 替换为你的CSV文件路径
groups = {
    'Group_1': csv_files[0:3],
    'Group_2': csv_files[4:6],
    'Group_3': csv_files[7:10],
    'Group_4': csv_files[11:14],
}

# 初始化一个列表，用于存储最终结果
final_results = []

# 遍历每个组
for group_name, group_files in groups.items():
    total_bias_points_sum = 0.0
    retweet_times_sum = 0.0

    # 遍历组中的每个文件
    for file in group_files:
        df = pd.read_csv(file)

        # 累加total_bias_points和retweet_times
        total_bias_points_sum += df['total_bias_points'].sum()
        retweet_times_sum += df['retweet_times'].sum()

    # 计算结果
    if retweet_times_sum != 0:
        group_result = total_bias_points_sum / retweet_times_sum
    else:
        group_result = 0  # 如果retweet_times_sum为0，避免除以0的错误

    # 将结果添加到最终结果列表中
    final_results.append([group_name, group_result])

# 将结果写入新的CSV文件
output_df = pd.DataFrame(final_results, columns=['Group', 'Bias Points per Retweet'])
output_df.to_csv('final_results.csv', index=False)

print("Data processing completed, results saved to 'final_results.csv'")

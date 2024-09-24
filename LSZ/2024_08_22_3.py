import os
import pandas as pd

# 设置文件夹路径
folder_path = r"F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\2_monthly_users_bias"

# 定义各个阶段的时间段
stages = {
    "第一阶段": ["2019_12", "2020_01", "2020_02", "2020_03"],
    "第二阶段": ["2020_04", "2020_05", "2020_06"],
    "第三阶段": ["2020_07", "2020_08", "2020_09", "2020_10"],
    "第四阶段": ["2020_11", "2020_12", "2021_01", "2021_02"]
}

# 读取每个阶段的用户集合A
stage_users_files = {
    "第一阶段": "第一阶段_users.csv",
    "第二阶段": "第二阶段_users.csv",
    "第三阶段": "第三阶段_users.csv",
    "第四阶段": "第四阶段_users.csv"
}

# 对每个阶段进行处理
for stage, months in stages.items():
    # 读取用户集合A
    users_a_file = os.path.join(folder_path, stage_users_files[stage])
    users_a = pd.read_csv(users_a_file)['user_id'].astype(str).tolist()

    # 初始化用户的总分和总次数
    total_bias_points = {user_id: 0 for user_id in users_a}
    retweet_times = {user_id: 0 for user_id in users_a}

    # 遍历阶段中的每个月
    for month in months:
        file_path = os.path.join(folder_path, f"{month}_output.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            # 计算总分和总次数
            for _, row in df.iterrows():
                user_id = row['retweeted_user_id']
                if user_id in users_a:
                    total_bias_points[user_id] += row['total_bias_points']
                    retweet_times[user_id] += row['retweet_times']

    # 计算每个用户的政治倾向平均值
    average_bias_points = {}
    for user_id in users_a:
        if retweet_times[user_id] > 0:
            average_bias_points[user_id] = total_bias_points[user_id] / retweet_times[user_id]
        else:
            average_bias_points[user_id] = 0.0  # 如果总次数为0，则平均值设为0

    # 保存结果到CSV文件
    output_file = os.path.join(folder_path, f"{stage}_average_bias.csv")
    result_df = pd.DataFrame({
        'retweeted_user_id': users_a,
        'total_bias_points': [total_bias_points[user_id] for user_id in users_a],
        'retweet_times': [retweet_times[user_id] for user_id in users_a],
        'average_bias_points': [average_bias_points[user_id] for user_id in users_a]
    })
    result_df.to_csv(output_file, index=False)

    print(f"{stage} 平均政治倾向结果已保存到: {output_file}")
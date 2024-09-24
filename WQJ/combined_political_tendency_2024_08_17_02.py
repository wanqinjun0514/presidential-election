import os
import pandas as pd

# 定义文件路径和阶段划分
file_dir = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\2_monthly_users_bias'
file_list = sorted(os.listdir(file_dir))  # 排序文件名
stages = {
    1: file_list[:4],   # 第1阶段: 文件1-4
    2: file_list[4:7],  # 第2阶段: 文件5-7
    3: file_list[7:11], # 第3阶段: 文件8-11
    4: file_list[11:15] # 第4阶段: 文件12-15
}

# 第一步：统计每个阶段中每个月都有政治倾向的用户
stage_users = {}
for stage, files in stages.items():
    stage_data = []
    for file in files:
        df = pd.read_csv(os.path.join(file_dir, file))
        stage_data.append(set(df['retweeted_user_id']))
    stage_users[stage] = set.intersection(*stage_data)  # 每个阶段所有月都有数据的用户

    # 保存阶段用户集合到csv
    pd.DataFrame({'retweeted_user_id': list(stage_users[stage])}).to_csv(f'stage_{stage}_users.csv', index=False)

# 第二步：计算每个阶段的用户的总分、总次数以及平均值
stage_user_stats = {}
for stage, users in stage_users.items():
    total_bias = {}
    total_retweets = {}

    for file in stages[stage]:
        df = pd.read_csv(os.path.join(file_dir, file))
        df = df[df['retweeted_user_id'].isin(users)]
        for _, row in df.iterrows():
            user_id = row['retweeted_user_id']
            total_bias[user_id] = total_bias.get(user_id, 0) + row['total_bias_points']
            total_retweets[user_id] = total_retweets.get(user_id, 0) + row['retweet_times']

    # 计算平均值并保存
    avg_bias_points = {user_id: total_bias[user_id] / total_retweets[user_id] for user_id in users}
    result_df = pd.DataFrame({
        'retweeted_user_id': list(users),
        'total_bias_points': [total_bias[user] for user in users],
        'retweet_times': [total_retweets[user] for user in users],
        'average_bias_points': [avg_bias_points[user] for user in users]
    })
    result_df.to_csv(f'stage_{stage}_user_stats.csv', index=False)
    stage_user_stats[stage] = avg_bias_points

# 第三步：统计两个阶段之间相同的用户集合及其平均值对比
for stage1 in range(1, 5):
    for stage2 in range(stage1 + 1, 5):
        common_users = stage_users[stage1].intersection(stage_users[stage2])
        result_df = pd.DataFrame({
            'two_stages_same_user_id': list(common_users),
            'stage1_average_bias_points': [stage_user_stats[stage1][user] for user in common_users],
            'stage2_average_bias_points': [stage_user_stats[stage2][user] for user in common_users]
        })
        result_df.to_csv(f'common_users_stage_{stage1}_vs_{stage2}.csv', index=False)

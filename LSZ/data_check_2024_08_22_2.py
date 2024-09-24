import os
import pandas as pd
from collections import defaultdict

# 第一步，用之前统计出来的每个月的用户政治倾向的文件（例如，without_url部分的数据统计的每个月用户政治倾向文件在F:\Experimental #Results\Average_Bias_Rating\politician_average_rating\without_url-rating\2_monthly_users_bias下，表头是#retweeted_user_id,total_bias_points,retweet_times,average_bias_points），用这些文件统计出每个阶段里每一个月都有政治倾向的用户，这些用户作为该阶段的用
# 户集合A。
# 设置文件夹路径
folder_path = r"F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\2_monthly_users_bias"

# 定义各个阶段的时间段
stages = {
    "第一阶段": ["2019_12", "2020_01", "2020_02", "2020_03"],
    "第二阶段": ["2020_04", "2020_05", "2020_06"],
    "第三阶段": ["2020_07", "2020_08", "2020_09", "2020_10"],
    "第四阶段": ["2020_11", "2020_12", "2021_01", "2021_02"]
}

# 初始化字典用于存储每个阶段的用户
stage_users = {stage: defaultdict(int) for stage in stages}

# 遍历文件夹中的所有CSV文件
for filename in os.listdir(folder_path):
    if filename.endswith("_output.csv"):
        # 提取文件名中的年月信息
        year_month = filename.split("_output.csv")[0]

        # 判断该文件属于哪个阶段
        for stage, months in stages.items():
            if year_month in months:
                # 读取CSV文件
                file_path = os.path.join(folder_path, filename)
                df = pd.read_csv(file_path)

                # 统计用户在每个阶段的出现次数
                for user_id in df['retweeted_user_id']:
                    stage_users[stage][user_id] += 1

# 过滤出每个月都有数据的用户，并持久化到本地
for stage, user_dict in stage_users.items():
    total_months = len(stages[stage])
    # 选出在每个月都有数据的用户
    users_in_all_months = [user for user, count in user_dict.items() if count == total_months]

    # 将用户集合保存到本地
    output_file = os.path.join(folder_path, f"{stage}_users.csv")
    pd.DataFrame(users_in_all_months, columns=["user_id"]).to_csv(output_file, index=False)

    print(f"{stage} 用户集合已保存到: {output_file}")

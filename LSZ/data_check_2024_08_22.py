import os
import pandas as pd


##统计三个部分数据里被打上分的推文的数量，用打分好的文件统计出retweet_times列的总和
# 文件夹路径
# folder_path = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\2_monthly_users_bias'
# folder_path = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\twitter_url-rating'
folder_path = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\external_url-rating'
# 获取文件夹中的所有CSV文件
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 初始化结果字典
results = {}

# 遍历每个CSV文件
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    # 读取csv文件的第三列
    df = pd.read_csv(file_path, usecols=[2])
    # 将列名改为方便访问的名字
    df.columns = ['retweet_times']
    # 计算第三列的总和
    total_sum = df['retweet_times'].sum()

    # 将结果保存到字典中，键为文件名（去掉后缀），值为总和
    month = os.path.splitext(file)[0]
    results[month] = total_sum

# 输出结果
for month, total in results.items():
    # print(f"{month}: {total}")
    print(f"{total}")
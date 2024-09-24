import os
import pandas as pd

# 文件夹路径
folder_path = rf'F:\three_parts_output\without_url'

# 获取所有子文件夹
subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]

# 初始化结果字典
results = {}

# 遍历每个子文件夹
for subfolder in subfolders:
    # 初始化一个集合用于存储不重复的retweeted_user_id
    unique_user_ids = set()

    # 遍历子文件夹中的所有csv文件
    for file in os.listdir(subfolder):
        if file.endswith('.csv'):
            file_path = os.path.join(subfolder, file)
            # 读取csv文件的第三列
            df = pd.read_csv(file_path, usecols=[2], dtype=str)
            # 将列名改为方便访问的名字
            df.columns = ['retweeted_user_id']
            # 将retweeted_user_id添加到集合中
            unique_user_ids.update(df['retweeted_user_id'].dropna())

    # 统计不重复的retweeted_user_id的个数
    month = os.path.basename(subfolder)
    results[month] = len(unique_user_ids)

# 输出结果
for month, count in results.items():
    print(f"{count}")
    # print(f"{month}: {count}")
#在F:\Experimental Results\Average_Bias_Rating\media_average_rating下面有四个文件夹，分别名为external_url-rating、multiple_url-rating、twitter_url-rating和without_url-rating。这四个文件夹下面都有一个名为quarterly_user_bias_scores的文件夹，里面保存了六部分数据，其命名形如：quarterly_user_bias_scores_2019_12_2020_01_2020_02.csv、quarterly_user_bias_scores_2020_03_2020_04_2020_05.csv、quarterly_user_bias_scores_2020_06_2020_07_2020_08.csv、quarterly_user_bias_scores_2020_09_2020_10.csv、quarterly_user_bias_scores_2020_11_2020_12.csv、quarterly_user_bias_scores_2021_01_2021_02.csv。对于每一个csv，它的表头是user_id,total_score,appearance_count,average_bias_points。我们平行合并四个文件夹中六部分的数据。例如，我们先处理四个文件夹中的quarterly_user_bias_scores_2019_12_2020_01_2020_02.csv，我们将其中出现的每个user_id累加total_score和appearance_count，最后用total_score除以appearance_count得到average_bias_points。请注意，user_id可能只在四个文件夹其中一个或多个的数据中出现。

#将六部分的结果以csv形式写入F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\user_bias_scores_by_quarter。

import os
import pandas as pd

# 定义输入文件夹路径
input_folders = [
    r"F:\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating\quarterly_user_bias_scores",
    r"F:\Experimental Results\Average_Bias_Rating\media_average_rating\multiple_url-rating\quarterly_user_bias_scores",
    r"F:\Experimental Results\Average_Bias_Rating\media_average_rating\twitter_url-rating\quarterly_user_bias_scores",
    r"F:\Experimental Results\Average_Bias_Rating\media_average_rating\without_url-rating\quarterly_user_bias_scores"
]

# 定义输出文件夹路径
output_folder = r"F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\user_bias_scores_by_quarter"

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 定义需要处理的文件名列表
file_names = [
    "quarterly_user_bias_scores_2019_12_2020_01_2020_02.csv",
    "quarterly_user_bias_scores_2020_03_2020_04_2020_05.csv",
    "quarterly_user_bias_scores_2020_06_2020_07_2020_08.csv",
    "quarterly_user_bias_scores_2020_09_2020_10.csv",
    "quarterly_user_bias_scores_2020_11_2020_12.csv",
    "quarterly_user_bias_scores_2021_01_2021_02.csv"
]

# 遍历每个文件
for file_name in file_names:
    merged_data = {}

    # 遍历每个文件夹
    for folder in input_folders:
        file_path = os.path.join(folder, file_name)

        if os.path.exists(file_path):
            # 读取csv文件，并将user_id作为字符串类型处理
            df = pd.read_csv(file_path, dtype={'user_id': str})

            # 累加每个user_id的total_score和appearance_count
            for _, row in df.iterrows():
                user_id = row['user_id']
                total_score = row['total_score']
                appearance_count = row['appearance_count']

                if user_id not in merged_data:
                    merged_data[user_id] = {'total_score': 0, 'appearance_count': 0}

                merged_data[user_id]['total_score'] += total_score
                merged_data[user_id]['appearance_count'] += appearance_count

    # 计算average_bias_points并保存为DataFrame
    final_data = []
    for user_id, scores in merged_data.items():
        total_score = scores['total_score']
        appearance_count = scores['appearance_count']
        average_bias_points = total_score / appearance_count if appearance_count != 0 else 0
        final_data.append([user_id, total_score, appearance_count, average_bias_points])

    # 创建DataFrame，将user_id显式转换为字符串
    result_df = pd.DataFrame(final_data, columns=['user_id', 'total_score', 'appearance_count', 'average_bias_points'])
    result_df['user_id'] = result_df['user_id'].astype(str)

    # 保存结果到csv
    output_file_path = os.path.join(output_folder, file_name)
    result_df.to_csv(output_file_path, index=False)

print("所有文件处理完成并保存到目标文件夹。")

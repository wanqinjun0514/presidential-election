#在F:\Experimental Results\Average_Bias_Rating\media_average_rating路径下，有四个文件夹，代表四部分数据。这四个文件夹中各有一个名为user_bias_scores_by_month的文件夹。这四个文件夹中的user_bias_scores_by_month文件夹下，都有2019年12月到2021年2月一共15个月的用户数据。其命名为user_bias_scores_2019_12.csv到user_bias_scores_2021_02.csv。csv的表头为user_id,total_score,appearance_count,average_bias_points。
#我们平行处理四个文件夹中每个月的用户数据。对于每个月，我们将四个csv中都出现的user_id提取出来，将四个csv中的total_score累加，将四个csv中的appearance_count累加。最后用累加的total_score除以累加的appearance_count得到average_bias_points。最终每个月处理的结果作为一个csv保存到F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\user_bias_scores_by_month下面。

import os
import pandas as pd
from functools import reduce
from concurrent.futures import ProcessPoolExecutor

# 文件夹路径
folders = [
    r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating\user_bias_scores_by_month',
    r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\multiple_url-rating\user_bias_scores_by_month',
    r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\twitter_url-rating\user_bias_scores_by_month',
    r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\without_url-rating\user_bias_scores_by_month'
]

# 输出文件夹路径
output_folder = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\user_bias_scores_by_month'
os.makedirs(output_folder, exist_ok=True)

# 获取每个月的CSV文件名称
months = [f"user_bias_scores_{year}_{month:02d}.csv" for year in range(2019, 2022) for month in range(1, 13) if not (year == 2019 and month < 12) and not (year == 2021 and month > 2)]


def process_month(month):
    # 读取每个月的四个文件，确保user_id为字符串
    dfs = [pd.read_csv(os.path.join(folder, month), dtype={'user_id': str}) for folder in folders]

    # 使用concat合并四个数据框，按user_id进行去重，形成并集
    combined_df = pd.concat(dfs, ignore_index=True).groupby('user_id', as_index=False).agg({
        'total_score': 'sum',
        'appearance_count': 'sum'
    })

    # 计算新的 average_bias_points
    combined_df['average_bias_points'] = combined_df['total_score'] / combined_df['appearance_count']

    # 保存处理后的CSV文件
    output_file = os.path.join(output_folder, month)
    combined_df[['user_id', 'total_score', 'appearance_count', 'average_bias_points']].to_csv(output_file, index=False)




for month in months:
    process_month(month)
print("所有月份的数据处理完成并保存。")

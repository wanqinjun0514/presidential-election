import os
import pandas as pd

# 定义目录路径
# input_dir = r'G:\four\Experimental Results\Average_Bias_Rating\media_average_rating\twitter_url-rating'
# output_dir = r'G:\four\Experimental Results\Average_Bias_Rating\media_average_rating\twitter_url-rating\processed'
# input_dir = r'G:\four\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating'
# output_dir = r'G:\four\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating\processed'
# input_dir = r'G:\four\Experimental Results\Average_Bias_Rating\media_average_rating\without_url-rating'
# output_dir = r'G:\four\Experimental Results\Average_Bias_Rating\media_average_rating\without_url-rating\processed'
input_dir = r'G:\four\Experimental Results\Average_Bias_Rating\media_average_rating\multiple_url-rating'
output_dir = r'G:\four\Experimental Results\Average_Bias_Rating\media_average_rating\multiple_url-rating\processed'
# 创建输出目录（如果不存在）
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 遍历目录下的所有CSV文件
for filename in os.listdir(input_dir):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_dir, filename)

        # 读取CSV文件，并明确指定每列的数据类型
        df = pd.read_csv(file_path, dtype={'user_id': str, 'total_score': int, 'appearance_count': int})

        # 检查表头是否包含所需的列
        if 'total_score' in df.columns and 'appearance_count' in df.columns:
            # 计算average_bias_points，避免除以零的情况
            df['average_bias_points'] = df['total_score'] / df['appearance_count'].replace(0, float('nan'))

            # 确保average_bias_points是float类型
            df['average_bias_points'] = df['average_bias_points'].astype(float)

            # 保存处理后的CSV到新目录
            output_file_path = os.path.join(output_dir, filename)
            df.to_csv(output_file_path, index=False)
            print(f"Processed and saved: {output_file_path}")
        else:
            print(f"Skipped {filename}: missing required columns.")

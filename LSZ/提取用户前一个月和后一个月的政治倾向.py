import pandas as pd
import os

#这是一个Python数据处理任务，在F:\Experimental Results\Average_Bias_Rating\politician_average_rating\twitter_url-rating文件夹下面，有15个月份（2019年12月到2021年2月）的csv文件，csv文件形如2019_12_output.csv。
#csv文件的表头形如retweeted_user_id,total_bias_points,retweet_times,average_bias_points。其中第一列格式为string，其它为float。我们会用到第一列和第四列。对于第四列average_bias_points，它的值在-1到1之间。我们把-1到0作为左，0到1作为右。
#对于连在一起的每两个月，寻找都出现了的retweeted_user_id，将前面那个月和后面那个月的average_bias_points记录下来，写入到F:\Experimental Results\Average_Bias_Rating\politician_average_rating\twitter_url-rating\sankey_plot\common_user_bias下面的一个csv里面。
#所以最终，我们应当得到14个csv文件，它们的命名形如：common_user_bias_2019_12_to_2020_01.csv，表头形如：retweeted_user_id,month1_average,month2_average。

# 文件夹路径
# input_folder = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\external_url-rating'
# input_folder = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\twitter_url-rating'
input_folder = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\2_monthly_users_bias'
output_folder = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\sankey_plot\common_user_bias'


# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 获取月份文件
months = [f"{y}_{m:02d}_output.csv" for y in range(2019, 2022) for m in range(1, 13) if not (y == 2021 and m > 2)]

# 处理每对相邻的月份
for i in range(len(months) - 1):
    # 获取前后两个月的文件名
    month1_file = months[i]
    month2_file = months[i + 1]

    # 读取两个月的数据
    month1_path = os.path.join(input_folder, month1_file)
    month2_path = os.path.join(input_folder, month2_file)

    if not os.path.exists(month1_path) or not os.path.exists(month2_path):
        continue

    # 只读取需要的列
    df_month1 = pd.read_csv(month1_path, usecols=['retweeted_user_id', 'average_bias_points'])
    df_month2 = pd.read_csv(month2_path, usecols=['retweeted_user_id', 'average_bias_points'])

    # 合并两个DataFrame，寻找共同的retweeted_user_id
    common_users = pd.merge(df_month1, df_month2, on='retweeted_user_id', suffixes=('_month1', '_month2'))

    # 写入结果文件
    output_file = f"common_user_bias_{month1_file[:-11]}_to_{month2_file[:-11]}.csv"
    output_path = os.path.join(output_folder, output_file)
    common_users.to_csv(output_path, index=False)

    print(f"Saved: {output_file}")



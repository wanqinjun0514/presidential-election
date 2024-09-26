import os
import pandas as pd
# 统计单个文件夹里的文件行数
# 用来统计三个部分数据里被打上分的统计打分的用户量有多少
def rated_users_counts():
    # folder_path = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\2_monthly_users_bias'
    # folder_path = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\twitter_url-rating'
    # folder_path = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\external_url-rating'
    # folder_path = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating'
    # folder_path = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\multiple_url-rating'
    folder_path = r'F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Media'

    # 创建一个空字典来存储文件名和对应的行数
    file_row_counts = {}

    # 遍历文件夹中的所有CSV文件
    for filename in os.listdir(folder_path):
        # if filename.startswith('common_user_bias_'):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            # 读取CSV文件
            df = pd.read_csv(file_path)
            # 统计除表头外的行数
            row_count = len(df)
            # 将结果存储在字典中
            file_row_counts[filename] = row_count

    # 打印结果
    for file, count in file_row_counts.items():
        # print(f'File: {file}, Number of Rows (excluding header): {count}')
        print(f'{count}')
        # print(f'{file}:  {count}')


# 对F:\Intermediate Results\Average_Bias_Rating\politician_influence_output\具体转贴和引贴的统计  这个文件夹下的所有csv进行数据统计，每个csv的表头都是“文件名,转发次数,引用次数,转贴和引用次数”这四列数据，我现在需要把每个csv里的每一行的转发次数,引用次数,转贴和引用次数这三列数据依次做累加
# 最后得到每个csv里的总转发次数,总引用次数,总转贴和引用次数
def 统计一个文件夹下所有csv的某列数据之和():
    # 定义文件夹路径
    folder_path = r'F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Politician\twitter_url\简化转发关系里的具体转贴和引贴的统计'

    # 初始化一个字典，用来存储每个文件的统计结果
    summary_dict = {}

    # 遍历文件夹下的所有CSV文件
    for filename in os.listdir(folder_path):
        if filename.startswith("矩阵分解方法的之前的简化转发关系统计_"):
            file_path = os.path.join(folder_path, filename)

            # 读取CSV文件
            df = pd.read_csv(file_path)
            print('正在处理文件', file_path)
            # 计算总转发次数、引用次数和转贴和引用次数
            total_reposts = df['转发次数'].sum()
            total_quotes = df['引用次数'].sum()
            total_reposts_and_quotes = df['转贴和引用次数'].sum()

            # 将结果存储在字典中
            summary_dict[filename] = {
                '总转发次数': total_reposts,
                '总引用次数': total_quotes,
                '总转贴和引用次数': total_reposts_and_quotes
            }

    # 将结果转换为DataFrame以便查看
    summary_df = pd.DataFrame.from_dict(summary_dict, orient='index')

    # 将结果保存为CSV文件
    output_file = r'F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Politician\twitter_url\简化转发关系里的具体转贴和引贴的统计\twitter_url具体转贴和引贴的统计汇总summary_results.csv'
    summary_df.to_csv(output_file, encoding='utf-8-sig')

    print(f'统计结果已保存到 {output_file}')



# 实现对F:\three_parts_output\single_url\twitter_url下的所有文件夹里的所有csv的函数统计，输出一个月份里所有csv文件行数累加和，即每个月的数据量做一个统计
def count_csv_rows_in_months():
    base_folder = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating'
    # 存储每个月的统计结果
    monthly_row_counts = {}

    # 遍历base_folder中的每个文件夹（每个文件夹代表一个月份）
    for month_folder in os.listdir(base_folder):
        month_path = os.path.join(base_folder, month_folder)

        # 确保这是一个文件夹
        if os.path.isdir(month_path):
            total_rows = 0  # 用于存储当前月份的总行数
            print("正在处理文件夹：",month_path)
            # 遍历当前月份文件夹中的每个CSV文件
            for csv_file in os.listdir(month_path):
                if csv_file.endswith('.csv'):
                    csv_path = os.path.join(month_path, csv_file)

                    # 使用pandas读取CSV文件并统计行数，解决DtypeWarning和tokenizing错误
                    try:
                        df = pd.read_csv(csv_path, dtype=str, low_memory=False)
                        total_rows += len(df)
                    except Exception as e:
                        print(f"读取文件 {csv_file} 时出现错误: {e}")

            # 将该月份的总行数添加到统计结果中
            monthly_row_counts[month_folder] = total_rows

    # 输出每个月的统计结果
    for month, row_count in monthly_row_counts.items():
        print(f"月份: {month}, 总行数: {row_count}")

    return monthly_row_counts

# 统计一下F:\three_parts_output\single_url\external_url\output_2019_12下的所有csv里的retweeted_user_id数量。具体步骤应该是初始化一个retweeted_user_id的字典，遍历所有的csv，遇到了一个新的retweeted_user_id就加入字典，遇到了retweeted_user_id在字典中就跳过，最后统计出了output_2019_12文件夹下所有的用户集合，输出用户数量给我
def all_output_users_count():
    # 初始化文件夹路径和retweeted_user_id字典
    months = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
              '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']
    for month in months:
        folder_path = rf"F:\three_parts_output\single_url\external_url\output_{month}"
        retweeted_user_id_dict = {}

        # 遍历文件夹下所有的csv文件
        for file in os.listdir(folder_path):
            if file.endswith('.csv'):
                file_path = os.path.join(folder_path, file)
                df = pd.read_csv(file_path,dtype=str)

                # 检查文件中是否有'retweeted_user_id'列
                if 'retweeted_user_id' in df.columns:
                    for user_id in df['retweeted_user_id']:
                        # 如果user_id不在字典中，加入字典
                        if user_id not in retweeted_user_id_dict:
                            retweeted_user_id_dict[user_id] = True
        # 统计用户数量
        unique_user_count = len(retweeted_user_id_dict)
        print(f'{month}里的用户数量有： ',unique_user_count)




# 帮我统计一下F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\user_bias_scores_by_month目录下的所有csv文件的每个csv文件的appearance_count列的值之和，给我每个csv一个appearance_count列的总数
def 文件夹下每个csv文件的某列之和():
    # 指定目录路径
    directory = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\user_bias_scores_by_month'

    # 存储每个文件的 appearance_count 总数
    results = {}

    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            # 读取 CSV 文件
            df = pd.read_csv(file_path)

            # 确保 appearance_count 列存在
            if 'appearance_count' in df.columns:
                total_count = df['appearance_count'].sum()
                results[filename] = total_count
            else:
                results[filename] = 'appearance_count 列不存在'

    # 输出结果
    for file, total in results.items():
        # print(f"{file}\t{total}")
        print(f"{total}")


if __name__ == '__main__':
    rated_users_counts()   # 统计单个文件夹里的文件行数
    # 统计一个文件夹下所有csv的某列数据之和()
    # count_csv_rows_in_months()
    # all_output_users_count()
    # 文件夹下每个csv文件的某列之和()
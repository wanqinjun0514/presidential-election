import os
import pandas as pd



def every_mouth_data():
    # 设置主文件夹路径
    main_folder_path = 'F:\\us-presidential-output'

    # 创建一个空的列表来保存结果
    result_list = []

    # 遍历主文件夹内的每个子文件夹
    for subfolder in os.listdir(main_folder_path):
        subfolder_path = os.path.join(main_folder_path, subfolder)
        # print(subfolder_path)
        if os.path.isdir(subfolder_path):
            total_rows = 0
            # 遍历子文件夹内的每个CSV文件
            for file in os.listdir(subfolder_path):
                if file.endswith('.csv'):
                    file_path = os.path.join(subfolder_path, file)
                    # print(file_path)
                    df = pd.read_csv(file_path, dtype=str)
                    total_rows += len(df)
            # 将每个子文件夹的总行数添加到结果列表中
            result_list.append(total_rows)
            print(f"子文件夹 '{subfolder}' 内所有CSV文件的行数总和为: {total_rows}")

    # 计算 result_list 中所有数值的总和
    total_sum = 0
    for value in result_list:
        total_sum += value
    print(f"所有子文件夹内CSV文件的行数总和为: {total_sum}")

    return result_list

def appearance_count_all():
    # 指定文件夹路径
    folder_path = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating'

    # 初始化总和
    total_sum = 0

    # 遍历文件夹下所有CSV文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            # 构建完整的文件路径
            file_path = os.path.join(folder_path, filename)

            # 读取CSV文件
            df = pd.read_csv(file_path)

            # 计算第三列的和
            column_sum = df.iloc[:, 2].sum()

            # 输出中间结果
            print(f'{filename}的第三列之和: {column_sum}')

            # 累加到总和
            total_sum += column_sum

    # 输出总和
    print(f'所有CSV文件的第三列数据之和: {total_sum}')



# 实现从两个csv文件里匹配数据，统计出一个总数出来。具体步骤是：读取F:\Experimental Results\media-only-url-bias-final-url.csv，这个文件的表头是domain,bias。读取F:\Experimental Results\accumulated_url_without_twitter_counts.csv，这个文件的表头是Domain,Count。现在需要在accumulated_url_without_twitter_counts.csv里的Domain列里找出所有media-only-url-bias-final-url.csv里的domain，找到之后将找到的Domain对应的Count累加起来。同时需要输出一些中间结果以便我检查结果，每在accumulated_url_without_twitter_counts.csv里匹配到一条Domain就输出这个Domain和Count
def check_media_count():
    # 读取CSV文件
    bias_df = pd.read_csv(r'F:\Experimental Results\media-only-url-bias-final-url.csv')
    count_df = pd.read_csv(r'F:\Experimental Results\accumulated_url_without_twitter_counts.csv')

    # 初始化总计数和匹配到的Domain数量
    total_count = 0
    matched_domains_count = 0

    # 遍历bias_df的每一个domain
    for domain in bias_df['domain']:
        # 在count_df中查找是否存在这个domain
        match = count_df[count_df['Domain'] == domain]

        # 如果找到匹配的domain
        if not match.empty:
            count_value = match['Count'].values[0]
            print(f'Matched Domain: {domain}, Count: {count_value}')
            total_count += count_value
            matched_domains_count += 1

    # 输出总数和匹配到的Domain数量
    print(f'Total Count: {total_count}')
    print(f'Total Matched Domains: {matched_domains_count}')



if __name__ == '__main__':

    # output_result = every_mouth_data()

    appearance_count_all()

    # check_media_count()








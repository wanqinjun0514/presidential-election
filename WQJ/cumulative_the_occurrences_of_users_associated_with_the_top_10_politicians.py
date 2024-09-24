import os
import csv
from collections import defaultdict



# 现在需要完成的统计任务是：
# 需要遍历F:\Intermediate Results\top10_politician_related_users(need_to_check)\external_url文件夹下的所有csv，每个csv的表头都是：retweeted_user_id,associated_retweet_origin_user_id,count。
# 我需要统计出这些csv里所有相同的associated_retweet_origin_user_id对应的count总和。
# 程序的具体步骤是：
# 构建一个字典（由associated_retweet_origin_user_id映射到count）
# 读取每个csv里的每一行数据，判断这一行数据的associated_retweet_origin_user_id字段的值是否在字典里，如果在字典里就将当前行的count字段累加到字典里的associated_retweet_origin_user_id映射的count上；
# 如果associated_retweet_origin_user_id字段的值不在字典里，将associated_retweet_origin_user_id字段添加到字典里，这个字段对应的count的值初始是0，再累加上这一行的count，即就是这一行的count
# 最终将这个associated_retweet_origin_user_id映射到count的字典输出到一个csv里
#################################################################
# 目的是：需要检查前10的次数累加起来，看看和combine之前的csv里统计的count数量能不能对应上
def statitic_three_parts():
    # 定义输入文件夹路径和输出文件路径
    input_folder = r'F:\Intermediate Results\top10_politician_related_users(need_to_check)\without_url'
    output_file = r'F:\Intermediate Results\top10_politician_related_users(need_to_check)\without_url_summary.csv'

    # 使用defaultdict来存储associated_retweet_origin_user_id到count的映射
    retweet_count_dict = defaultdict(int)

    # 遍历文件夹下的所有csv文件
    for filename in os.listdir(input_folder):
        if filename.endswith('_top_10_associations_with_counts.csv'):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    # 获取associated_retweet_origin_user_id和count字段的值
                    associated_retweet_origin_user_id = str(row['associated_retweet_origin_user_id'])  # 转换为str类型
                    count = int(row['count'])

                    # 累加count到字典中对应的associated_retweet_origin_user_id
                    retweet_count_dict[associated_retweet_origin_user_id] += count

    # 将结果输出到一个新的csv文件中
    with open(output_file, mode='w', newline='', encoding='utf-8') as output_csv:
        fieldnames = ['associated_retweet_origin_user_id', 'total_count']
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)

        writer.writeheader()
        for associated_retweet_origin_user_id, total_count in retweet_count_dict.items():
            writer.writerow(
                {'associated_retweet_origin_user_id': associated_retweet_origin_user_id, 'total_count': total_count})

    print(f'统计结果已输出到 {output_file}')



def sum_three_parts():
    # 定义输入文件夹路径和输出文件路径
    input_folder = r'F:\Intermediate Results\top10_politician_related_users(need_to_check)'
    output_file = r'F:\Intermediate Results\top10_politician_related_users(need_to_check)\three_parts_summary.csv'

    # 使用defaultdict来存储associated_retweet_origin_user_id到count的映射
    retweet_count_dict = defaultdict(int)

    # 遍历文件夹下的所有csv文件
    for filename in os.listdir(input_folder):
        if filename.endswith('_url_summary.csv'):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    # 获取associated_retweet_origin_user_id和count字段的值
                    associated_retweet_origin_user_id = str(row['associated_retweet_origin_user_id'])  # 转换为str类型
                    count = int(row['total_count'])

                    # 累加count到字典中对应的associated_retweet_origin_user_id
                    retweet_count_dict[associated_retweet_origin_user_id] += count

    # 将结果输出到一个新的csv文件中
    with open(output_file, mode='w', newline='', encoding='utf-8') as output_csv:
        fieldnames = ['associated_retweet_origin_user_id', 'total_count']
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)

        writer.writeheader()
        for associated_retweet_origin_user_id, total_count in retweet_count_dict.items():
            writer.writerow(
                {'associated_retweet_origin_user_id': associated_retweet_origin_user_id, 'total_count': total_count})

    print(f'统计结果已输出到 {output_file}')


if __name__ == '__main__':
    sum_three_parts()
import os
import glob
import numpy as np
import pandas as pd

# 统计单个output文件的用户及用户出现次数，每个output.csv生成一个统计用户的csv
def count_user_id(csv_path, result_path):
    print(f"内容开始读取!")
    df = pd.read_csv(csv_path, header=0, dtype=str)
    print(f"内容读取成功!")

    line_num_before = 0
    line_num_after = 0

    pd.set_option('expand_frame_repr', False)
    # print(df)
    line_num_before = df.shape[0]

    selected_values = df.iloc[:, [2]].values
    np.set_printoptions(linewidth=500)
    # print(selected_values)

    value_counts = np.unique(selected_values, return_counts=True)
    # print(value_counts)

    result_df = pd.DataFrame({
        'Value': value_counts[0],
        'Count': value_counts[1]
    })

    # print(result_df)

    result_df = result_df.sort_values(by='Count', ascending=False)
    # print(result_df)
    line_num_after = result_df.shape[0]

    result_df.to_csv(result_path, index=False, header=True)

    return line_num_before, line_num_after

# 统计整个月份文件夹里的output文件的用户及用户出现次数，每个文件夹生成一个统计用户的csv
# （统计了转贴/引用推文的用户id及出现次数（字段：retweeted_user_id）、统计了被转发情况下的原帖用户id及出现次数（字段：retweet_origin_user_id）、统计了被引用情况下的原帖用户id及出现次数（字段：quoted_origin_user_id））
def count_user_id_in_folder(folder_path, result_path):
    all_results = pd.DataFrame()

    for csv_file in glob.glob(os.path.join(folder_path, '*-output.csv')):
        print(f"处理文件：{csv_file}")
        df = pd.read_csv(csv_file, header=0, dtype={'quoted_origin_user_id': str})  # 确保作为字符串读取
        df.dropna(subset=['quoted_origin_user_id'], inplace=True)

        # 直接使用pandas的value_counts进行统计，避免使用np.unique
        value_counts = df['quoted_origin_user_id'].value_counts().reset_index()
        value_counts.columns = ['Value', 'Count']  # 重命名列以匹配all_results的列名

        # 合并当前结果到总结果DataFrame中
        all_results = pd.concat([all_results, value_counts], ignore_index=True)

    # 汇总相同Value的Count值
    final_result = all_results.groupby('Value', as_index=False)['Count'].sum()
    final_result = final_result.sort_values(by='Count', ascending=False)

    # 保存汇总后的统计结果到CSV文件
    final_result.to_csv(result_path, index=False, header=True)
    print(f"所有文件统计结果已保存到：{result_path}")

#合并每个月份文件夹统计的folder-monthly-count-user-id.csv
def merge_csv_results(folder_path, final_result_path):
    # 初始化一个空的DataFrame用于存储合并后的数据
    merged_df = pd.DataFrame()
    # 匹配文件夹下所有以folder-monthly-count-user-id结尾的csv文件
    pattern = os.path.join(folder_path, '*folder-monthly-count-user-id.csv')
    for csv_file in glob.glob(pattern):
        print(f"正在读取文件：{csv_file}")
        # 读取当前csv文件
        current_df = pd.read_csv(csv_file, header=0, dtype={'Value':str,'Count':int})

        # 将当前文件的数据添加到merged_df中
        merged_df = pd.concat([merged_df, current_df], ignore_index=True)

    # 如果需要对合并后的数据进行进一步处理（例如汇总相同Value的Count值），可以在这里添加代码
    # 例如，下面的代码对所有Value相同的行进行Count值的求和
    final_result = merged_df.groupby('Value', as_index=False)['Count'].sum()
    print(final_result['Count'].sum())
    final_result = final_result.sort_values(by='Count', ascending=False)

    # 保存合并后的结果到新的CSV文件
    final_result.to_csv(final_result_path, index=False, header=True)
    print(f"合并后的结果已保存到：{final_result_path}")




if __name__ == "__main__":

    # count_user_id(r"H:\wqj_test\output_csv\2019-12-06-1-output.csv", r"H:\wqj_test\output_csv\2019-12-06-1-count-userid.csv")

    count_user_id_in_folder(r"H:\us-presidential-output\merge_2019_12",r"H:\record\count_user_id_record\origin_quote_user\2019_12-folder-monthly-count-user-id.csv")
    count_user_id_in_folder(r"H:\us-presidential-output\merge_2020_01",r"H:\record\count_user_id_record\origin_quote_user\2020_01-folder-monthly-count-user-id.csv")
    count_user_id_in_folder(r"H:\us-presidential-output\merge_2020_02",r"H:\record\count_user_id_record\origin_quote_user\2020_02-folder-monthly-count-user-id.csv")
    count_user_id_in_folder(r"H:\us-presidential-output\merge_2020_03",r"H:\record\count_user_id_record\origin_quote_user\2020_03-folder-monthly-count-user-id.csv")
    count_user_id_in_folder(r"H:\us-presidential-output\merge_2020_04",r"H:\record\count_user_id_record\origin_quote_user\2020_04-folder-monthly-count-user-id.csv")
    count_user_id_in_folder(r"H:\us-presidential-output\merge_2020_05",r"H:\record\count_user_id_record\origin_quote_user\2020_05-folder-monthly-count-user-id.csv")
    count_user_id_in_folder(r"H:\us-presidential-output\merge_2020_06",r"H:\record\count_user_id_record\origin_quote_user\2020_06-folder-monthly-count-user-id.csv")
    count_user_id_in_folder(r"H:\us-presidential-output\merge_2020_07",r"H:\record\count_user_id_record\origin_quote_user\2020_07-folder-monthly-count-user-id.csv")
    count_user_id_in_folder(r"H:\us-presidential-output\merge_2020_08",r"H:\record\count_user_id_record\origin_quote_user\2020_08-folder-monthly-count-user-id.csv")
    count_user_id_in_folder(r"H:\us-presidential-output\merge_2020_09",r"H:\record\count_user_id_record\origin_quote_user\2020_09-folder-monthly-count-user-id.csv")
    count_user_id_in_folder(r"H:\us-presidential-output\merge_2020_10",r"H:\record\count_user_id_record\origin_quote_user\2020_10-folder-monthly-count-user-id.csv")
    count_user_id_in_folder(r"H:\us-presidential-output\merge_2020_11",r"H:\record\count_user_id_record\origin_quote_user\2020_11-folder-monthly-count-user-id.csv")
    count_user_id_in_folder(r"H:\us-presidential-output\merge_2020_12",r"H:\record\count_user_id_record\origin_quote_user\2020_12-folder-monthly-count-user-id.csv")
    count_user_id_in_folder(r"H:\us-presidential-output\merge_2021_01",r"H:\record\count_user_id_record\origin_quote_user\2021_01-folder-monthly-count-user-id.csv")
    count_user_id_in_folder(r"H:\us-presidential-output\merge_2020_02",r"H:\record\count_user_id_record\origin_quote_user\2021_02-folder-monthly-count-user-id.csv")
    # 合并
    merge_csv_results(r"H:\record\count_user_id_record\origin_quote_user",r"H:\record\count_user_id_record\origin_quote_user\total-count-origin-quote-user-id.csv")

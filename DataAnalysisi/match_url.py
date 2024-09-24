import chardet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




def match_url():

    csv_path = "H:\\with_url_data\\accumulated_url_without_twitter_counts.csv"
    xlsx_path = "H:\\with_url_data\\domain-url-bias.xlsx"

    df_csv = pd.read_csv(csv_path)
    df_xlsx = pd.read_excel(xlsx_path)

    # 准备一个空列表，用于存储更新后的行
    updated_rows = []

    # 迭代 CSV 文件中的每一行
    for index, row in df_csv.iterrows():
        domain_in_csv = row['Domain']

        # 检查 Domain 是否在 XLSX 文件的 URL 列中出现
        matched_rows = df_xlsx[df_xlsx['URL'].str.contains(domain_in_csv, na=False)]

        if not matched_rows.empty:
            # 如果找到匹配，取第一个匹配项的 'domain' 和 'bias'
            domain_in_xlsx = matched_rows.iloc[0]['domain']
            bias = matched_rows.iloc[0]['bias']
            # 将找到的数据添加到 CSV 行中
            updated_row = row.tolist() + [domain_in_xlsx, bias]
        else:
            # 如果没有找到匹配，保持原行不变，但添加两个空值以保持列对齐
            updated_row = row.tolist() + [None, None]

        updated_rows.append(updated_row)

    # 将更新后的行数据转换为 DataFrame
    updated_df_csv = pd.DataFrame(updated_rows, columns=df_csv.columns.tolist() + ['domain', 'bias'])

    # 保存更新后的 DataFrame 到新的 CSV 文件
    updated_csv_path = r'H:\with_url_data\updated_accumulated_url_without_twitter_counts.csv'
    updated_df_csv.to_csv(updated_csv_path, index=False)

    print("更新完成，保存至：", updated_csv_path)







if __name__ == "__main__":


    csv_path = "H:\\with_url_data\\updated_accumulated_url_without_twitter_counts.csv"
    output_csv_path = "H:\\with_url_data\\bias-None.xlsx.csv"

    df_csv = pd.read_csv(csv_path, header=0, nrows=200)
    print(df_csv)

    # sum_of_first_100 = df_csv['Count'].head(200).sum()
    # total_sum = df_csv['Count'].sum()
    #
    # print(sum_of_first_100)
    # print(total_sum)
    # print(sum_of_first_100/total_sum)

    bias_empty_rows = []

    for index, row in df_csv.iterrows():
        if pd.isnull(row["bias"]):
            bias_empty_rows.append(row)

    # 将列表转换为 DataFrame
    empty_rows_df = pd.DataFrame(bias_empty_rows)

    # 输出到一个新的 CSV 文件
    empty_rows_df.to_csv(output_csv_path, index=False)







    # # 计算整列的总和
    # total_sum = df_csv['Count'].sum()
    #
    # # 定义一个空的列表来存储比值
    # ratios = []
    #
    # # 定义最大行数，以及步长
    # max_rows = len(df_csv)
    # step = 1  # 可以根据你的需求调整步长
    #
    # # 计算不同行数的比值
    # for x in range(1, max_rows + 1, step):
    #     sum_of_first_x = df_csv['Count'].head(x).sum()
    #     ratio = sum_of_first_x / total_sum
    #     ratios.append(ratio)
    #
    # # 生成横坐标
    # x_values = list(range(1, max_rows + 1, step))
    #
    # # 绘图
    # plt.figure(figsize=(10, 6))
    # plt.plot(x_values, ratios, marker='o')
    # plt.title('比值 vs. 前 x 行数')
    # plt.xlabel('前 x 行数')
    # plt.ylabel('比值（前 x 行之和 / 总和）')
    # plt.grid(True)
    # plt.show()




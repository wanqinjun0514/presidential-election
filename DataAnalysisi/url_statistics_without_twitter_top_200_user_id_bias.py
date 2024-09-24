import os
from urllib.parse import urlparse
import pandas as pd
import re


# 根据top_200_url_bias_final.csv文件  将url媒体对用户的打分 记录retweeted_user_id, Domain, 和 bias
# 检查 retweet_url_array 和 quote_url_array 是否为空。如果不为空，代码会解析这些URL，并提取其域名。然后，它会检查这些域名是否存在于 domain_bias_dict 字典中
def url_count(date):
    # date = '2019_12'
    folder_path = f'H:\\us-presidential-output\\output_{date}'
    result_path = f'H:\\with_url_data\\without_twitter_top_884_user_id_bias\\matching_top_200_user_id_{date}.csv'
    # 设置显示选项
    pd.set_option('display.max_columns', None)  # 不限制列数
    pd.set_option('display.width', None)  # 根据内容自动调整输出宽度
    # 读取域名和偏见数据，并构建字典
    bias_data_path = "H:\\with_url_data\\new-domain-bias_final.csv"
    df_bias = pd.read_csv(bias_data_path)
    domain_bias_dict = pd.Series(df_bias.bias.values, index=df_bias.Domain).to_dict()

    # 初始化DataFrame来收集所有CSV文件的结果
    all_matching_data = []

    # 遍历文件夹下的所有CSV文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            print("------------------------------------------------------------------------------------------------------------------------------------")
            print(f"正在处理文件: {file_path}")
            df_cvs = pd.read_csv(file_path, header=0, dtype=str)

            # 提取需要的列
            selected_values = df_cvs.iloc[:, [1, 2, 8, 9, 18,
                                              19]].values  # 1 retweeted_id、2 retweeted_user_id、8 retweet_expanded_urls_array、9 retweet_origin_user_id、18 quoted_expanded_urls_array、19 quoted_origin_user_id
            line_num = selected_values.shape[0]
            print(f"总行数: {line_num}")

            # 遍历每行数据
            for i in range(line_num):
                if (i + 1) % 50000 == 0:
                    print(f"处理到第 {i + 1} 行")
                retweeted_id = selected_values[i, 0]
                retweeted_user_id = selected_values[i, 1]
                retweet_url_array = selected_values[i, 2]
                retweet_origin_user_id = selected_values[i, 3]
                quote_url_array = selected_values[i, 4]
                quoted_origin_user_id = selected_values[i, 5]

                # 检查URL数组是否为空，如果不为空，进行解析和处理
                for url_array in [retweet_url_array, quote_url_array]:
                    if pd.notna(url_array):
                        url_list = url_array.split(', ')
                        for url in url_list:
                            parsed_url = urlparse(url)
                            domain = parsed_url.netloc

                            if domain in domain_bias_dict:
                                # 如果域名存在于字典中，记录retweeted_user_id, Domain, 和 bias
                                bias = domain_bias_dict[domain]
                                all_matching_data.append(
                                    [retweeted_id, retweeted_user_id, domain, bias, retweet_origin_user_id,
                                     quoted_origin_user_id])

    # 将匹配的数据转换为DataFrame，并保存为CSV文件
    result_df = pd.DataFrame(all_matching_data, columns=['retweet_id', 'retweeted_user_id', 'Domain', 'bias', 'retweet_origin_user_id', 'quoted_origin_user_id'])
    result_df.to_csv(result_path, index=False)
    print("数据处理完成并已保存。")


# 统计csv一列数据的总和
def count_column_num():
    # 读取CSV文件
    df = pd.read_csv(
        r'G:\with_url_data\without_twitter_top_200_user_id_bias\media_user_bias_score\media_user_bias_2020_11.csv')
    # 计算第二列的总和
    # 假设我们不知道第二列的列名，可以使用iloc来按位置选择
    sum_column = df.iloc[:, 1].sum()

    print("第二列的数据总和是:", sum_column)


# 在检查媒体打标签步骤的数量对不对 统计G:\with_url_data\record\output_2019_12.txt里retweet_num_domain和quote_num_domain的数量
def count_num():
    file_path = r'G:\with_url_data\record\output_2019_12.txt'
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if 'retweet_num_domain' in line and 'quote_num_domain' in line:
                # Extract retweet_num_domain
                retweet_num_domain_start = line.index('retweet_num_domain: ') + len('retweet_num_domain: ')
                retweet_num_domain_end = line.index('\t', retweet_num_domain_start)
                retweet_num_domain = int(line[retweet_num_domain_start:retweet_num_domain_end].strip())

                # Extract quote_num_domain
                quote_num_domain_start = line.index('quote_num_domain: ') + len('quote_num_domain: ')
                quote_num_domain_end = line.index('\t', quote_num_domain_start)
                quote_num_domain = int(line[quote_num_domain_start:quote_num_domain_end].strip())

                # Store the extracted values
                data.append((retweet_num_domain, quote_num_domain))

    # Calculate the total sum of both retweet_num_domain and quote_num_domain
    total_retweet_num_domain = sum(x[0] for x in data)
    total_quote_num_domain = sum(x[1] for x in data)
    total_sum = total_retweet_num_domain + total_quote_num_domain
    print(total_retweet_num_domain)
    print(total_quote_num_domain)
    print(total_sum)


if __name__ == "__main__":

    folder_list = os.listdir("H:\\us-presidential-output")

    pattern = r'\d{4}_\d{2}'
    for date in folder_list:

        match = re.search(pattern, date)
        print("====================================================================================================================================")
        print(match.group())
        url_count(match.group())


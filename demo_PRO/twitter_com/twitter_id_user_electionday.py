import os
from urllib.parse import urlparse
import re
import pandas as pd
import numpy as np


def extract_id_user(xlsx_path, result_path):
    print(f"内容开始读取!")
    df = pd.read_excel(xlsx_path, sheet_name="Sheet1", header=None, dtype=str, )
    print(f"内容读取成功!")

    pd.set_option('display.width', None)
    pd.set_option('display.max_columns', None)
    # print(f"内容读取成功:\n{df}")
    # print("------------------------------------------------------------")

    selected_values = df.iloc[:, [5, 6, 7, 13, 14, 15]].values
    line_num = selected_values.shape[0]
    np.set_printoptions(linewidth=300)
    # print(selected_values)

    result_array = []

    line_count = 0
    url_count = 0

    for i in range(0, line_num):

        if i % 50000 == 0:  # 当i是50000的倍数时
            print(f"行数: {i}")

        if pd.notna(selected_values[i, 1]):
            line_count += 1
            url_list_0 = selected_values[i, 1].split(', ')
            for url in url_list_0:
                # 使用urlparse函数解析URL
                parsed_url = urlparse(url)
                # 提取域名
                domain = parsed_url.netloc
                # 判断域名是否为twitter.com
                if domain == "twitter.com":
                    # print(url, "的域名是 twitter.com")
                    match = re.search(r'https://twitter.com/(\w+)/status', url)
                    if match:
                        username = match.group(1)
                        new_row = [selected_values[i, 0],
                                   url,
                                   username,
                                   selected_values[i, 2]]
                    else:
                        username = "未找到用户名"
                        new_row = [selected_values[i, 0],
                                   url,
                                   username,
                                   selected_values[i, 2]]
                    result_array.append(new_row)
                    url_count += 1
        elif pd.notna(selected_values[i, 4]):
            line_count += 1
            url_list_1 = selected_values[i, 4].split(', ')
            for url in url_list_1:
                # 使用urlparse函数解析URL
                parsed_url = urlparse(url)
                # 提取域名
                domain = parsed_url.netloc
                # 判断域名是否为twitter.com
                if domain == "twitter.com":
                    # print(url, "的域名是 twitter.com")
                    match = re.search(r'https://twitter.com/(\w+)/status', url)
                    if match:
                        username = match.group(1)
                        new_row = [selected_values[i, 3],
                                   url,
                                   username,
                                   selected_values[i, 5]]
                    else:
                        username = "未找到用户名"
                        new_row = [selected_values[i, 3],
                                   url,
                                   username,
                                   selected_values[i, 5]]
                    result_array.append(new_row)
                    url_count += 1

    # for row in result_array:
    #     print(row)

    # 将数组转换为 DataFrame
    df_result = pd.DataFrame(result_array, columns=['retweet_id', 'url', 'username', 'user_id'])
    # print(df_result)

    # 存储 DataFrame 到 Excel 文件中
    df_result.to_excel(result_path, index=False, header=True)

    return line_count, url_count, line_num


def batch_extract_id_user(num_xlsx):
    record_txt = f'H:\\twitter_id_user\\electionday\\electionday.txt'

    for i in range(0, num_xlsx + 1):  # 生成0_output.xlsx-num_output.xslx
        input_xlsx = f"H:\\electionday\\electionday-filter-ids-ok-{i}.xlsx"
        output_xlsx = f'H:\\twitter_id_user\\electionday\\{i}.xlsx'
        print("-----------------------------------------------------------------------------------------------------")
        print(input_xlsx)
        print(output_xlsx)
        print(record_txt)
        line_count, url_count, line_num = extract_id_user(input_xlsx, output_xlsx, )

        with open(record_txt, 'a', encoding='utf-8') as rt:
            print_string = f"electionday-{i}：line_count: {line_count}\t\turl_count: {url_count}\t\tline_num: {line_num}\n"
            rt.write(print_string)


if __name__ == "__main__":

    print("=====================================================================================================")
    output_folder = f'H:\\twitter_id_user\\electionday'
    # 检查文件夹是否存在
    if not os.path.exists(output_folder):
        # 如果不存在，创建文件夹
        os.makedirs(output_folder)
        print(f"Folder '{output_folder}' created.")
    else:
        print(f"Folder '{output_folder}' already exists.")

    batch_extract_id_user(13)
    # extract_id_user("H:\\demo\\demo_split_output.xlsx", "H:\\result_twitter_id_user.xlsx")

# 该文件提取映射关系：被转发推文id ↔ url
# 未去重id

import os
from urllib.parse import urlparse
import pandas as pd


def extract_id_url(xlsx_path, result_path):
    print(f"内容开始读取!")
    df = pd.read_excel(xlsx_path, sheet_name="Sheet1", header=None, dtype=str, )
    print(f"内容读取成功!")

    # pd.set_option('display.max_columns', None)
    # # 打印表格内容
    # print(f"内容读取成功:\n{df}")
    # print("------------------------------------------------------------")

    # selected_values = df.iloc[:, [5, 6, 13, 14]].values
    selected_values = df.iloc[:, [5, 6]].values
    # print(selected_values)
    # print("------------------------------------------------------------")

    line_num = selected_values.shape[0]

    all_none_num = 0
    retweet_num = 0
    retweet_url = 0
    quote_num = 0
    quote_url = 0
    num = 0
    result_df = pd.DataFrame(columns=['ID', 'URL'])

    for i in range(0, line_num):
        num = num + 1
        if num % 50000 == 0:  # 当i是50000的倍数时
            print(f"行数: {num}")

        value_0 = str(selected_values[i, 0])
        # print(value_0)
        value_1 = selected_values[i, 1]
        # print(value_1)
        # value_2 = str(selected_values[i, 2])
        # # print(value_2)
        # value_3 = selected_values[i, 3]
        # # print(value_3)

        if pd.notna(value_1):
            # 如果只有第一列不为空，打印出不为空的元素
            retweet_num = retweet_num + 1

            url_list_1 = value_1.split(', ')
            for url in url_list_1:
                # print(url)
                # 使用urlparse函数解析URL
                parsed_url = urlparse(url)
                # 提取域名
                domain = parsed_url.netloc
                result_df = result_df._append({'ID': value_0, 'URL': domain}, ignore_index=True)
                retweet_url = retweet_url + 1


        # elif pd.notna(value_3):
        #     # 如果只有第二列不为空，打印出不为空的元素
        #     quote_num = quote_num + 1
        #
        #     url_list_3 = value_3.split(', ')
        #     for url in url_list_3:
        #         # print(url)
        #         # 使用urlparse函数解析URL
        #         parsed_url = urlparse(url)
        #         # 提取域名
        #         domain = parsed_url.netloc
        #         result_df = result_df._append({'ID': value_2, 'URL': domain}, ignore_index=True)
        #         quote_url = quote_url + 1

        else:
            # 如果两列都为空，其他处理
            all_none_num = all_none_num + 1

    result_df.to_excel(result_path, index=False)

    return all_none_num, retweet_num, retweet_url, quote_num, quote_url


def batch_extract_id_url(num_xlsx):
    record_txt = f'H:\\retweeted_id - url\\electionday\\electionday.txt'

    for i in range(0, num_xlsx + 1):  # 生成0_output.xlsx-num_output.xslx
        input_xlsx = f"H:\\electionday\\electionday-filter-ids-ok-{i}.xlsx"
        output_xlsx = f'H:\\retweeted_id - url\\electionday\\{i}.xlsx'
        print("-----------------------------------------------------------------------------------------------------")
        print(input_xlsx)
        print(output_xlsx)
        print(record_txt)
        all_none_num, retweet_num, retweet_url, quote_num, quote_url = extract_id_url(input_xlsx, output_xlsx, )

        with open(record_txt, 'a', encoding='utf-8') as rt:
            print_string = f"electionday-{i}：all_none_num: {all_none_num}\t\tretweet_num: {retweet_num}\t\tretweet_url: {retweet_url}\t\tquote_num: {quote_num}\t\tquote_url: {quote_url}\n"
            rt.write(print_string)


if __name__ == "__main__":

    print("=====================================================================================================")
    output_folder = f'H:\\retweeted_id - url\\electionday'
    # 检查文件夹是否存在
    if not os.path.exists(output_folder):
        # 如果不存在，创建文件夹
        os.makedirs(output_folder)
        print(f"Folder '{output_folder}' created.")
    else:
        print(f"Folder '{output_folder}' already exists.")

    batch_extract_id_url(13)

    # extract_id_url("H:\\demo.xlsx", "H:\\demo_result.xlsx")

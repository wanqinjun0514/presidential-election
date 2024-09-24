# 统计url，以及出现次数
import os
from urllib.parse import urlparse

import pandas as pd


def url_count(xlsx_path, result_path):

    print(f"内容开始读取!")
    df = pd.read_excel(xlsx_path, sheet_name="Sheet1", header=None)
    print(f"内容读取成功!")

    # 打印表格内容
    # print(f"内容读取成功:\n{df}")
    # print("------------------------------------------------------------")

    selected_values = df.iloc[:, [6, 14]].values

    # print(selected_values)
    # print("------------------------------------------------------------")

    line_num = selected_values.shape[0]

    domain_count = {}
    all_none_num = 0
    retweet_num = 0
    quote_num = 0
    all_no_none_num = 0
    all_no_none_index = []
    num = 0

    for i in range(0, line_num):
        num = num+1
        if num % 50000 == 0:  # 当i是50000的倍数时
            print(f"行数: {num}")

        value_0 = selected_values[i, 0]
        value_1 = selected_values[i, 1]
        url_list_0 = None
        url_list_1 = None

        # 检查是否为空
        if pd.notna(value_0) and pd.notna(value_1):
            # 如果不同时为空，其他处理，打印出不为空的元素
            all_no_none_num = all_no_none_num + 1
            all_no_none_index.append(i + 1)
            # print(f"第{i + 1}行的第一列和第二列都不为空，元素为: {value_0}, {value_1}")
            url_list_0 = value_0.split(', ')
            for url in url_list_0:
                # print(url)
                # 使用urlparse函数解析URL
                parsed_url = urlparse(url)
                # 提取域名
                domain = parsed_url.netloc
                # print(domain)
                if domain in domain_count:
                    domain_count[domain] += 1
                else:
                    domain_count[domain] = 1

            url_list_1 = value_1.split(', ')
            for url in url_list_1:
                # print(url)
                # 使用urlparse函数解析URL
                parsed_url = urlparse(url)
                # 提取域名
                domain = parsed_url.netloc
                # print(domain)
                if domain in domain_count:
                    domain_count[domain] += 1
                else:
                    domain_count[domain] = 1

        elif pd.notna(value_0):
            # 如果只有第一列不为空，打印出不为空的元素
            retweet_num = retweet_num + 1
            # print(f"第{i + 1}行的第一列不为空，元素为: {value_0}")
            url_list_0 = value_0.split(', ')
            for url in url_list_0:
                # print(url)
                # 使用urlparse函数解析URL
                parsed_url = urlparse(url)
                # 提取域名
                domain = parsed_url.netloc
                # print(domain)
                if domain in domain_count:
                    domain_count[domain] += 1
                else:
                    domain_count[domain] = 1

        elif pd.notna(value_1):
            # 如果只有第二列不为空，打印出不为空的元素
            quote_num = quote_num + 1
            # print(f"第{i + 1}行的第二列不为空，元素为: {value_1}")
            url_list_1 = value_1.split(', ')
            for url in url_list_1:
                # print(url)
                # 使用urlparse函数解析URL
                parsed_url = urlparse(url)
                # 提取域名
                domain = parsed_url.netloc
                # print(domain)
                if domain in domain_count:
                    domain_count[domain] += 1
                else:
                    domain_count[domain] = 1

        else:
            # 如果两列都为空，其他处理
            all_none_num = all_none_num + 1
            # print(f"第{i + 1}行的第一列和第二列都为空")
            # print("\n")

    # for domain, count in domain_count.items():
    #     print(f"{domain}: {count} 次")

    # 将字典转换为DataFrame
    df = pd.DataFrame(list(domain_count.items()), columns=["Domain", "Count"])

    # 保存DataFrame到Excel文件
    df.to_excel(result_path, index=False)

    return all_none_num, retweet_num, quote_num, all_no_none_num, all_no_none_index

    # with open(record_path, "a") as txt_file:
    #     txt_file.write(f"all_none_num: {all_none_num}\t")
    #     txt_file.write(f"retweet_num: {retweet_num}\t")
    #     txt_file.write(f"quote_num: {quote_num}\t")
    #     txt_file.write(f"all_no_none_num: {all_no_none_num}\t")
    #     txt_file.write(f"all_no_none_index: {all_no_none_index}\n")


def batch_url_count(num_file, num_xlsx):

    record_txt = f'H:\\url_statistics\\democratic\\{num_file}\\{num_file}.txt'

    for i in range(15, num_xlsx + 1):  # 生成0_output.xlsx-num_output.xslx
        input_xlsx = f"H:\\democratic\\democratic-candidate-filter-ids-{num_file}-output\\democratic-candidate-filter-ids-{num_file}-ok-{i}-output.xlsx"
        output_xlsx = f'H:\\url_statistics\\democratic\\{num_file}\\{num_file}-{i}.xlsx'
        print("-----------------------------------------------------------------------------------------------------")
        print(input_xlsx)
        print(output_xlsx)
        print(record_txt)
        all_none_num, retweet_num, quote_num, all_no_none_num, all_no_none_index = url_count(input_xlsx, output_xlsx,)

        with open(record_txt, 'a', encoding='utf-8') as rt:
            print_string = f"democratic-{num_file}-{i}：all_none_num: {all_none_num}\t\tretweet_num: {retweet_num}\t\tquote_num: {quote_num}\t\tall_no_none_num: {all_no_none_num}\t\tall_no_none_index: {all_no_none_index}\n"
            rt.write(print_string)


if __name__ == "__main__":
    # url_count("H:\\demo.xlsx", "H:\\demo_result.xlsx", "H:\\demo_record.txt")
    file_num = {
        3: 15,
        4: 15,
        5: 15,
        6: 14,
        7: 15,
        8: 15,
        9: 15,
        10: 15,
        11: 15,
        12: 15,
        13: 15,
        14: 15,
        15: 15,
        16: 14,
        17: 15,
    }

    for i in range(17, 18):

        print("=====================================================================================================")
        output_folder = f'H:\\url_statistics\\democratic\\{i}'
        # 检查文件夹是否存在
        if not os.path.exists(output_folder):
            # 如果不存在，创建文件夹
            os.makedirs(output_folder)
            print(f"Folder '{output_folder}' created.")
        else:
            print(f"Folder '{output_folder}' already exists.")

        batch_url_count(i, file_num[i])

import glob
import os
import re
from urllib.parse import urlparse

import pandas as pd


def url_count(cvs_path, domain_result_path, twitter_result_path):
    print(f"内容开始读取!")
    df_cvs = pd.read_csv(cvs_path, header=0, dtype=str)
    print(f"内容读取成功!")

    # 设置显示选项
    pd.set_option('display.max_columns', None)  # 不限制列数
    pd.set_option('display.width', None)  # 根据内容自动调整输出宽度

    # print(df_cvs)

    # 7:retweet_id
    # 8:retweet_expanded_urls_array
    # 9:retweet_origin_user_id
    # 17：quoted_id
    # 18：quoted_expanded_urls_array
    # 19：quoted_origin_user_id
    selected_values = df_cvs.iloc[:, [7, 8, 9, 17, 18, 19]].values

    # for i in selected_values:
    #     print(i)

    line_num = selected_values.shape[0]
    print(line_num)

    twitter_count = []
    twitter_url_count = 0

    domain_count = {}
    all_none_num = 0
    retweet_num = 0
    retweet_num_domain = 0
    retweet_num_twitter = 0
    quote_num = 0
    quote_num_domain = 0
    quote_num_twitter = 0
    all_no_none_num = 0
    all_no_none_index = []
    num = 0

    for i in range(0, line_num):
        num = num + 1
        if num % 50000 == 0:  # 当i是50000的倍数时
            print(f"行数: {num}")

        retweet_url_array = selected_values[i, 1]
        quote_url_array = selected_values[i, 4]

        # print(retweet_url_array)
        # print(quote_url_array)
        # 检查是否为空''
        if pd.notna(retweet_url_array) and pd.notna(quote_url_array):
            # 如果不同时为空，其他处理，打印出不为空的元素
            all_no_none_num = all_no_none_num + 1
            all_no_none_index.append(i + 1)
            # print(f"第{i + 1}行的第一列和第二列都不为空，元素为: {retweet_url_array}, {quote_url_array}")
            url_list_0 = retweet_url_array.split(', ')
            for url in url_list_0:
                # print(url)
                # 使用urlparse函数解析URL
                parsed_url = urlparse(url)
                # 提取域名
                domain = parsed_url.netloc
                # print(domain)

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
                    twitter_count.append(new_row)
                    twitter_url_count += 1
                else:
                    if domain in domain_count:
                        domain_count[domain] += 1
                    else:
                        domain_count[domain] = 1

            url_list_1 = quote_url_array.split(', ')
            for url in url_list_1:
                # print(url)
                # 使用urlparse函数解析URL
                parsed_url = urlparse(url)
                # 提取域名
                domain = parsed_url.netloc
                # print(domain)

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
                    twitter_count.append(new_row)
                    twitter_url_count += 1
                else:
                    if domain in domain_count:
                        domain_count[domain] += 1
                    else:
                        domain_count[domain] = 1

        elif pd.notna(retweet_url_array):
            # 如果只有第一列不为空，打印出不为空的元素
            retweet_num = retweet_num + 1
            # print(f"第{i + 1}行的第一列不为空，元素为: {retweet_url_array}")
            url_list_0 = retweet_url_array.split(', ')
            for url in url_list_0:
                # print(url)
                # 使用urlparse函数解析URL
                parsed_url = urlparse(url)
                # 提取域名
                domain = parsed_url.netloc
                # print(domain)
                if domain == "twitter.com":
                    retweet_num_twitter += 1
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
                    twitter_count.append(new_row)
                    twitter_url_count += 1
                else:
                    retweet_num_domain += 1
                    if domain in domain_count:
                        domain_count[domain] += 1
                    else:
                        domain_count[domain] = 1

        elif pd.notna(quote_url_array):
            # 如果只有第二列不为空，打印出不为空的元素
            quote_num = quote_num + 1
            # print(f"第{i + 1}行的第二列不为空，元素为: {quote_url_array}")
            url_list_1 = quote_url_array.split(', ')
            for url in url_list_1:
                # print(url)
                # 使用urlparse函数解析URL
                parsed_url = urlparse(url)
                # 提取域名
                domain = parsed_url.netloc
                # print(domain)
                if domain == "twitter.com":
                    quote_num_twitter += 1
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
                    twitter_count.append(new_row)
                    twitter_url_count += 1
                else:
                    quote_num_domain += 1
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

    # for i in twitter_count:
    #     print(i)

    # 将字典转换为DataFrame
    domain_count_df = pd.DataFrame(list(domain_count.items()), columns=['Domain', 'Count'])
    print(domain_count_df)

    # 将数组转换为 DataFrame
    twitter_count_df = pd.DataFrame(twitter_count, columns=['retweet_id', 'url', 'username', 'user_id'])
    print(twitter_count_df)

    # 将DataFrame保存为CSV文件
    domain_count_df.to_csv(domain_result_path, index=False, header=True)

    twitter_count_df.to_csv(twitter_result_path, index=False, header=True)

    print(f"line num: {line_num}\t\tall_none_num: {all_none_num}\t\tretweet num: {retweet_num}\t\tquote_num: {quote_num}\t\tall_no_none_num: {all_no_none_num}")

    return (all_none_num,
            retweet_num, retweet_num_domain, retweet_num_twitter,
            quote_num, quote_num_domain, quote_num_twitter,
            all_no_none_num, all_no_none_index)


def batch_url_count(folder_path, folder_name):
    record_txt = f'H:\\with_url_data\\record\\{folder_name}.txt'

    for cvs_name in os.listdir(folder_path):
        print("---------------------------------------------------------------------------------------------------")
        print(cvs_name)
        cvs_path_batch = os.path.join(folder_path, cvs_name)

        domain_dir_name = folder_name.replace("output_", "").replace("_", "-")
        domain_new_filename = cvs_name.replace("output", "domain")
        domain_full_dir_path = os.path.join("H:\\with_url_data\\with_twitter", domain_dir_name)
        if not os.path.exists(domain_full_dir_path):
            os.makedirs(domain_full_dir_path)
        domain_result_path_batch = os.path.join(domain_full_dir_path, domain_new_filename)

        twitter_dir_name = folder_name.replace("output_", "").replace("_", "-")
        twitter_new_filename = cvs_name.replace("output", "twitter")
        twitter_full_dir_path = os.path.join("H:\\with_url_data\\without_twitter", twitter_dir_name)
        if not os.path.exists(twitter_full_dir_path):
            os.makedirs(twitter_full_dir_path)
        twitter_result_path_batch = os.path.join(twitter_full_dir_path, twitter_new_filename)

        print(record_txt)
        print(cvs_path_batch)
        print(domain_result_path_batch)
        print(twitter_result_path_batch)
        (all_none_num,
         retweet_num, retweet_num_domain, retweet_num_twitter,
         quote_num, quote_num_domain, quote_num_twitter,
         all_no_none_num, all_no_none_index) = url_count(cvs_path_batch, domain_result_path_batch,
                                                         twitter_result_path_batch)

        with open(record_txt, 'a', encoding='utf-8') as rt:
            print_string = (f"{cvs_name}：all_none_num: {all_none_num}\t\t"
                            f"retweet_num: {retweet_num}\t\tretweet_num_domain: {retweet_num_domain}\t\tretweet_num_twitter: {retweet_num_twitter}\t\t"
                            f"quote_num: {quote_num}\t\tquote_num_domain: {quote_num_domain}\t\tquote_num_twitter:{quote_num_twitter}\t\t"
                            f"all_no_none_num: {all_no_none_num}\t\tall_no_none_index: {all_no_none_index}\n")
            rt.write(print_string)

    # with open(record_txt, 'a', encoding='utf-8') as rt:
    #     rt.write(f"{folder_name}")


if __name__ == "__main__":
    path = "H:\\us-presidential-output"
    for root, dirs, files in os.walk(path):
        for name in dirs:
            folder = os.path.join(root, name)
            print("===================================================================================================")
            print(name)
            batch_url_count(folder, name)

    # # batch_url_count("H:\\demo_data", "")
    # url_count("H:\\demo_data\\2019-12-01-2-output.csv", "H:\\demo_data\\1.csv", "H:\\demo_data\\2.csv")

# 1.10重新提取json中的数据

import json
import pandas as pd
import os
import glob


def extract_txt_to_csv(input_file, output_file):
    data_list = []      # 创建一个空的data_list列表，用于存储从txt文件中提取的数据
    all_line = 0
    retweet_line = 0    # 统计转贴的帖子数量有多少
    quote_line = 0      # 统计引用的帖子数量有多少
    reply_line = 0     # 统计回复的帖子数量有多少
    not_reply_line = 0 #非回复数量

    with open(input_file, 'r', encoding='utf-8') as f:

        for line in f:
            all_line += 1
            if all_line % 50000 == 0:  # 当i是50000的倍数时
                print(f"{input_file} 处理到行数: {all_line}（当i是50000的倍数时才输出）")
            # 当前帖子的信息
            retweeted_time = None
            retweeted_id = None
            retweeted_username = None
            retweeted_user_id = None
            retweeted_user_location = None
            retweeted_full_text = None
            retweeted_hashtags = None
            # 转发关系的原帖信息
            retweet_time = None
            retweet_id = None
            retweet_origin_username = None
            retweet_origin_user_id = None
            retweet_origin_user_location = None
            retweet_expanded_urls_array = None
            retweet_origin_user_intro_expanded_url = None
            retweet_origin_user_des_expanded_url = None
            retweet_origin_retweet_count = None
            retweeted_origin_full_text = None
            retweet_origin_hashtags = None
            # 引用关系的原帖信息
            quoted_time = None
            quoted_id = None
            quoted_origin_username = None
            quoted_origin_user_id = None
            quoted_origin_user_location = None
            quoted_expanded_urls_array = None
            quoted_origin_user_intro_expanded_url = None
            quoted_origin_user_des_expanded_url = None
            quoted_origin_retweet_count = None
            quoted_origin_full_text = None
            quoted_origin_hashtags = None

            obj = json.loads(line)
            in_reply_to_status_id_str = obj.get('in_reply_to_status_id_str', None)  # 帖子是否是回复别人的帖子（就是评论）
            if in_reply_to_status_id_str:  # 该字段不为空，则代表帖子是评论
                reply_line += 1
            else:  # 该字段为空，则代表不是评论
                not_reply_line += 1
                retweeted_full_text = obj.get('full_text', None)  # 转帖帖子的完整内容
                # 如果 full_text 不是 None，去除其中的空行
                if retweeted_full_text is not None:
                    # 替换掉字符串中的 '\r\n' 和 '\n' 以去除空行
                    retweeted_full_text = retweeted_full_text.replace('\r\n', ' ').replace('\n', ' ')
                retweeted_time = obj.get('created_at', None)  # 转帖时间
                retweeted_id = obj.get('id_str', None)  # 转贴id
                retweeted_entities = obj.get('entities', None)  # 转贴entities
                if retweeted_entities:
                    retweeted_hashtags = retweeted_entities.get('hashtags', None)  # 转贴hashtags
                    if not quoted_origin_hashtags:
                        retweeted_hashtags = None
                retweeted_user = obj.get('user', None)  # 转贴用户信息
                if retweeted_user:
                    retweeted_user_id = retweeted_user.get('id_str', None)  # 转贴用户的id
                    retweeted_username = retweeted_user.get('name', None)  # 转贴用户名称
                    retweeted_user_location = retweeted_user.get('location', None)  # 转贴用户设置的位置

                # 转贴
                origin_retweet = obj.get('retweeted_status', None)  # 原贴信息
                if origin_retweet:
                    retweet_line += 1
                    retweet_time = origin_retweet.get('created_at', None)  # 原帖创建时间
                    retweet_id = origin_retweet.get('id_str', None)  # 原帖id
                    retweeted_origin_full_text = origin_retweet.get('full_text', None)  # 原推帖子的完整内容
                    # 如果 full_text 不是 None，去除其中的空行
                    if retweeted_origin_full_text is not None:
                        # 替换掉字符串中的 '\r\n' 和 '\n' 以去除空行
                        retweeted_origin_full_text = retweeted_origin_full_text.replace('\r\n', ' ').replace('\n', ' ')
                        # print(retweeted_origin_full_text)

                    retweet_origin_entities = origin_retweet.get('entities', None)  # 原帖内容信息
                    if retweet_origin_entities:
                        retweet_origin_urls = retweet_origin_entities.get('urls', None)  # 原帖中的urls
                        retweet_origin_hashtags = retweet_origin_entities.get('hashtags', None)  # 原推帖子的hashtags
                        if not retweet_origin_hashtags:
                            retweet_origin_hashtags = None
                        if retweet_origin_urls:
                            retweet_expanded_urls_array = []
                            for url_info in retweet_origin_urls:
                                expanded_url = url_info.get('expanded_url', None)
                                if expanded_url:
                                    retweet_expanded_urls_array.append(expanded_url)

                    retweet_origin_user = origin_retweet.get('user', None)  # 原帖用户信息
                    if retweet_origin_user:
                        retweet_origin_user_id = retweet_origin_user.get('id_str', None)
                        retweet_origin_user_location = retweet_origin_user.get('location', None)
                        retweet_origin_user_entities = retweet_origin_user.get('entities', None)
                        retweet_origin_username = retweet_origin_user.get('name', None)

                        retweet_origin_user_intro_url = retweet_origin_user_entities.get('url', None)
                        if retweet_origin_user_intro_url:
                            retweet_origin_user_intro_urls = retweet_origin_user_intro_url.get('urls', None)
                            if retweet_origin_user_intro_urls and len(retweet_origin_user_intro_urls) > 0:
                                retweet_origin_user_intro_expanded_url = retweet_origin_user_intro_urls[0].get(
                                    'expanded_url', None)
                            else:
                                retweet_origin_user_intro_expanded_url = None

                        retweet_origin_user_description = retweet_origin_user_entities.get('description', None)
                        if retweet_origin_user_description:
                            retweet_origin_user_des_urls = retweet_origin_user_description.get('urls', None)
                            if retweet_origin_user_des_urls and len(retweet_origin_user_des_urls) > 0:
                                retweet_origin_user_des_expanded_url = retweet_origin_user_des_urls[0].get(
                                    'expanded_url', None)
                            else:
                                retweet_origin_user_des_expanded_url = None
                    retweet_origin_retweet_count = origin_retweet.get('retweet_count', None)

                # 引用
                origin_quoted = obj.get('quoted_status', None)
                if origin_quoted:
                    quote_line += 1
                    quoted_time = origin_quoted.get('created_at', None)
                    quoted_id = origin_quoted.get('id_str', None)
                    quoted_origin_full_text = origin_quoted.get('full_text', None)  # 引用的原推帖子的完整内容
                    # 如果 full_text 不是 None，去除其中的空行
                    if quoted_origin_full_text is not None:
                        # 替换掉字符串中的 '\r\n' 和 '\n' 以去除空行
                        quoted_origin_full_text = quoted_origin_full_text.replace('\r\n', ' ').replace('\n', ' ')
                        # print(quoted_origin_full_text)
                    quoted_origin_entities = origin_quoted.get('entities', None)
                    if quoted_origin_entities:
                        quoted_origin_urls = quoted_origin_entities.get('urls', None)
                        quoted_origin_hashtags = quoted_origin_entities.get('hashtags', None)
                        if not quoted_origin_hashtags:
                            quoted_origin_hashtags = None
                        if quoted_origin_urls:
                            quoted_expanded_urls_array = []
                            for url_info in quoted_origin_urls:
                                expanded_url = url_info.get('expanded_url', None)
                                if expanded_url:
                                    quoted_expanded_urls_array.append(expanded_url)

                    quoted_origin_user = origin_quoted.get('user', None)  # 原帖用户信息
                    if quoted_origin_user:
                        quoted_origin_user_id = quoted_origin_user.get('id_str', None)
                        quoted_origin_user_location = quoted_origin_user.get('location', None)
                        quoted_origin_user_entities = quoted_origin_user.get('entities', None)
                        quoted_origin_username = quoted_origin_user.get('name', None)

                        quoted_origin_user_intro_url = quoted_origin_user_entities.get('url', None)
                        if quoted_origin_user_intro_url:
                            quoted_origin_user_intro_urls = quoted_origin_user_intro_url.get('urls', None)
                            if quoted_origin_user_intro_urls and len(quoted_origin_user_intro_urls) > 0:
                                quoted_origin_user_intro_expanded_url = quoted_origin_user_intro_urls[0].get(
                                    'expanded_url', None)
                            else:
                                quoted_origin_user_intro_expanded_url = None

                        quoted_origin_user_description = quoted_origin_user_entities.get('description', None)
                        if quoted_origin_user_description:
                            quoted_origin_user_des_urls = quoted_origin_user_description.get('urls', None)
                            if quoted_origin_user_des_urls and len(quoted_origin_user_des_urls) > 0:
                                quoted_origin_user_des_expanded_url = quoted_origin_user_des_urls[0].get('expanded_url',
                                                                                                         None)
                            else:
                                quoted_origin_user_des_expanded_url = None
                    quoted_origin_retweet_count = origin_quoted.get('retweet_count', None)  # 原帖用户信息

                # print(retweeted_origin_full_text)
                # print(quoted_origin_full_text)

                data_list.append(
                    {
                        # 当前帖子的信息
                        'retweeted_time': retweeted_time,                                                               # A 转帖/引用帖子的时间
                        'retweeted_id': retweeted_id,                                                                   # B 转贴/引用帖子的推文id
                        'retweeted_user_id': retweeted_user_id,                                                         # C 转贴/引用帖子的用户id
                        'retweeted_username': retweeted_username,                                                       # D 转贴/引用帖子的用户名
                        'retweeted_user_location': retweeted_user_location,                                             # E 转贴/引用帖子的用户位置
                        'retweeted_full_text': retweeted_full_text,                                                     # F 转贴/引用的帖子的完整内容（full_text字段放在最后三列里）
                        'retweeted_hashtags': retweeted_hashtags,                                                       # G 转贴/引用的帖子的hashtags

                        # 转发关系的原帖信息
                        'retweet_time': retweet_time,                                                                   # H 被转贴的推文创建时间
                        'retweet_id': retweet_id,                                                                       # I 被转贴的推文id
                        'retweet_expanded_urls_array': retweet_expanded_urls_array,                                     # J 被转贴的推文中的url
                        'retweet_origin_user_id': retweet_origin_user_id,                                               # K 被转贴的推文发布者id
                        'retweet_origin_username': retweet_origin_username,                                             # L 被转贴的推文发布者用户名
                        'retweet_origin_user_location': retweet_origin_user_location,                                   # M 被转贴的推文发布者位置
                        'retweet_origin_user_intro_expanded_url': retweet_origin_user_intro_expanded_url,               # N 被转贴的推文发布者设置中的url
                        'retweet_origin_user_des_expanded_url': retweet_origin_user_des_expanded_url,                   # O 被转贴的推文发布者描述中的url
                        'retweet_origin_retweet_count': retweet_origin_retweet_count,                                   # P 被转贴的推文帖子的转发次数
                        'retweeted_origin_full_text': retweeted_origin_full_text,                                       # Q 被转贴的推文帖子的完整内容（full_text字段放在最后三列里）
                        'retweet_origin_hashtags': retweet_origin_hashtags,                                             # R 被转贴帖子的hashtags

                        # 引用关系的原帖信息
                        'quoted_time': quoted_time,                                                                     # S 被引用的推文创建时间
                        'quoted_id': quoted_id,                                                                         # T 被引用的推文id
                        'quoted_expanded_urls_array': quoted_expanded_urls_array,                                       # U 被引用的推文中的url
                        'quoted_origin_user_id': quoted_origin_user_id,                                                 # V 被引用的推文发布者id
                        'quoted_origin_username': quoted_origin_username,                                               # W 被引用的推文发布者用户名
                        'quoted_origin_user_location': quoted_origin_user_location,                                     # X 被引用的推文发布者位置
                        'quoted_origin_user_intro_expanded_url': quoted_origin_user_intro_expanded_url,                 # Y 被引用的推文发布者设置中的url
                        'quoted_origin_user_des_expanded_url': quoted_origin_user_des_expanded_url,                     # Z 被引用的推文发布者描述中的url
                        'quoted_origin_retweet_count': quoted_origin_retweet_count,                                     # AA 被引用的推文帖子的引用次数
                        'quoted_origin_full_text': quoted_origin_full_text,                                             # AB 被引用的推文帖子的完整内容（full_text字段放在最后三列里）
                        'quoted_origin_hashtags': quoted_origin_hashtags,                                               # AC 被引用的帖子的hashtags
                    })

    print(
        "-----------------------------------------------------------------------------------------------------------------------------")
    # print(data_list)

    # for i in data_list:
    #     print(i)

    print("all line:", all_line, "\tretweet_line:", retweet_line, "\tquote_line:", quote_line, "\tnot_reply_line:", not_reply_line, "\treply_line:", reply_line)

    df = pd.DataFrame(data_list, columns=[
        'retweeted_time', 'retweeted_id', 'retweeted_user_id', 'retweeted_username', 'retweeted_user_location',
        'retweeted_hashtags',
        'retweet_time', 'retweet_id', 'retweet_expanded_urls_array',
        'retweet_origin_user_id', 'retweet_origin_username', 'retweet_origin_user_location',
        'retweet_origin_user_intro_expanded_url', 'retweet_origin_user_des_expanded_url',
        'retweet_origin_retweet_count', 'retweet_origin_hashtags',
        'quoted_time', 'quoted_id', 'quoted_expanded_urls_array',
        'quoted_origin_user_id', 'quoted_origin_username', 'quoted_origin_user_location',
        'quoted_origin_user_intro_expanded_url', 'quoted_origin_user_des_expanded_url', 'quoted_origin_retweet_count',
        'quoted_origin_hashtags',
        'retweeted_full_text', 'retweeted_origin_full_text', 'quoted_origin_full_text',
    ])
    pd.set_option('expand_frame_repr', False)
    # print(df)

    df['retweet_expanded_urls_array'] = df['retweet_expanded_urls_array'].apply(
        lambda x: ', '.join(x) if isinstance(x, list) else x)
    df['quoted_expanded_urls_array'] = df['quoted_expanded_urls_array'].apply(
        lambda x: ', '.join(x) if isinstance(x, list) else x)
    df.to_csv(output_file, index=False, header=True)
    print("extract_txt_to_csv 已完成:", input_file)

    return all_line, retweet_line, quote_line, reply_line


# 将所有txt里运行了extract_txt_to_csv函数后的返回值保存在一个以当前folder_path命名的txt文件里
def batch_process_monthly_data(folder_path):
    # 从folder_path获取记录文件的名称
    folder_name = os.path.basename(folder_path)
    print("正在处理文件夹：",folder_name)
    record_file_path = os.path.join(r"H:\record\extract_record", f"{folder_name}_record.txt")
    # 遍历文件夹中所有以-merged-ok.txt结尾的文件
    # 开始处理每个文件，并收集结果
    with open(record_file_path, 'w', encoding='utf-8') as record_file:
        for input_file in glob.glob(os.path.join(folder_path, '*-merged-ok.txt')):
            base_name = os.path.basename(input_file)
            print("正在处理文件：",base_name)
            file_identifier = base_name.replace('-merged-ok.txt', '')
            output_csv_file = os.path.join(r"H:\us-presidential-output",folder_name, f"{file_identifier}-output.csv")

            # 调用extract_txt_to_csv函数并获取返回值
            all_line, retweet_line, quote_line, reply_line = extract_txt_to_csv(input_file, output_csv_file)
            print("正在将提取的csv文件保存至：", output_csv_file)
            print(f"文件夹:{folder_path} 里的 {input_file} -> {output_csv_file} 的提取已完成")
            # 将结果写入记录文件
            record_file.write(f"{base_name}: all_line={all_line},retweet_line={retweet_line},quote_line={quote_line} ,reply_line={reply_line}\n")
            print("提取的csv记录文件保存至：", record_file_path)

#统计所有merge_年份_月份_record的all_line,retweet_line,quote_line,reply_line
def merge_all_line_retweet_line_quote_line_reply_line_record():
    # 定义待处理的文件名列表
    file_names = [r'H:\record\extract_record\merge_2019_12_record.txt', r'H:\record\extract_record\merge_2020_01_record.txt', r'H:\record\extract_record\merge_2020_02_record.txt',
                  r'H:\record\extract_record\merge_2020_03_record.txt', r'H:\record\extract_record\merge_2020_04_record.txt', r'H:\record\extract_record\merge_2020_05_record.txt',
                  r'H:\record\extract_record\merge_2020_06_record.txt', r'H:\record\extract_record\merge_2020_07_record.txt', r'H:\record\extract_record\merge_2020_08_record.txt',
                  r'H:\record\extract_record\merge_2020_09_record.txt', r'H:\record\extract_record\merge_2020_10_record.txt', r'H:\record\extract_record\merge_2020_11_record.txt',
                  r'H:\record\extract_record\merge_2020_12_record.txt',
                  r'H:\record\extract_record\merge_2021_01_record.txt',
                  r'H:\record\extract_record\merge_2021_02_record.txt',
                  ]  # 请将这些文件名替换为实际的文件名
    # 打开一个新文件用于写入汇总结果
    with open(r'H:\record\extract_record\summary_merge_all_months_record.txt', 'w') as summary_file:
        # 遍历每个文件
        for file_name in file_names:
            # 初始化累加器
            all_line_sum = 0
            retweet_line_sum = 0
            quote_line_sum = 0
            reply_line_sum = 0

            # 打开并读取当前文件
            with open(file_name, 'r') as file:
                for line in file:
                    parts = line.split(',')
                    for part in parts:
                        if 'all_line' in part:
                            all_line_sum += int(part.split('=')[1])
                        elif 'retweet_line' in part:
                            retweet_line_sum += int(part.split('=')[1])
                        elif 'quote_line' in part:
                            quote_line_sum += int(part.split('=')[1])
                        elif 'reply_line' in part:
                            reply_line_sum += int(part.split('=')[1])

            # 将当前文件的统计结果写入汇总文件
            summary_file.write(
                f"{file_name}: all_line={all_line_sum}, retweet_line={retweet_line_sum}, quote_line={quote_line_sum}, reply_line={reply_line_sum}\n")

#对统计后的summary_merge_all_months_record.txt再进行累加统计，直接将结果输出到终端里
def final_result_all_line_retweet_line_quote_line_reply_line_output_to_terminal():
    # 定义文件名
    file_name = r'H:\record\extract_record\summary_merge_all_months_record.txt'
    # 初始化累加器
    all_line_sum = 0
    retweet_line_sum = 0
    quote_line_sum = 0
    reply_line_sum = 0
    # 打开文件并读取每一行
    with open(file_name, 'r') as file:
        for line in file:
            # 根据最新的格式调整，这里使用包含空格的关键词进行分割和匹配
            parts = line.split(',')
            for part in parts:
                if 'all_line' in part:
                    all_line_sum += int(part.split('=')[1])
                elif 'retweet_line' in part:
                    retweet_line_sum += int(part.split('=')[1])
                elif 'quote_line' in part:
                    quote_line_sum += int(part.split('=')[1])
                elif 'reply_line' in part:
                    reply_line_sum += int(part.split('=')[1])

        # 输出累加的结果
        print(f"all_line总和: {all_line_sum}")
        print(f"retweet_line总和: {retweet_line_sum}")
        print(f"quote_line总和: {quote_line_sum}")
        print(f"reply_line总和: {reply_line_sum}")

#统计merge步骤的数据，H:\record\monthly_merge_txt_record文件夹下的all_months_merge_txt_total_record.txt
def statistic_all_months_merge_txt_total_record():
    # 定义文件名
    file_name = r'H:\record\monthly_merge_txt_record\all_months_merge_txt_total_record.txt'
    # 初始化累加器
    num_line_sum = 0
    # 打开文件并读取每一行
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')  # 假设每个字段之间是通过制表符分隔的
            for part in parts:
                if 'num_line:' in part:
                    num_line_sum += int(part.split(':')[1].strip())  # 提取数值并累加
    # 输出累加的结果
    print(f"num_line总和: {num_line_sum}")



if __name__ == "__main__":
    # monthly_folder_paths = [
    #                         r'H:\us-presidential\merge_2020_04', r'H:\us-presidential\merge_2020_05',
    #                         r'H:\us-presidential\merge_2020_06', r'H:\us-presidential\merge_2020_07',
    #                         r'H:\us-presidential\merge_2020_12',
    #                         r'H:\us-presidential\merge_2021_01', r'H:\us-presidential\merge_2021_02',
    #                         ]
    # # monthly_folder_paths =[r'I:\2019-12-test_extract']
    # for folder_path in monthly_folder_paths:
    #     batch_process_monthly_data(folder_path)
    # merge_all_line_retweet_line_quote_line_reply_line_record()
    # final_result_all_line_retweet_line_quote_line_reply_line_output_to_terminal()
    statistic_all_months_merge_txt_total_record()
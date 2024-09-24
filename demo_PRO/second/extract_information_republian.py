# 1.10重新提取json中的数据

import json
import pandas as pd
import os

from openpyxl.workbook import Workbook


def extract_txt_to_xlsx(input_file, output_file):
    data_list = []  # 创建一个空的data_list列表，用于存储从txt文件中提取的数据
    all_line = 0
    true_line = 0

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            all_line += 1
            if all_line % 50000 == 0:  # 当i是50000的倍数时
                print(f"行数: {all_line}")

            obj = None

            retweeted_time = None
            retweeted_id = None
            retweeted_user = None
            retweeted_user_id = None
            retweeted_user_location = None

            origin_retweet = None
            retweet_time = None
            retweet_id = None
            retweet_origin_entities = None
            retweet_origin_urls = None
            retweet_origin_user = None
            retweet_origin_user_id = None
            retweet_origin_user_location = None
            retweet_origin_user_entities = None
            retweet_expanded_urls_array = None
            retweet_origin_user_intro_url = None
            retweet_origin_user_intro_urls = None
            retweet_origin_user_intro_expanded_url = None
            retweet_origin_user_description = None
            retweet_origin_user_des_urls = None
            retweet_origin_user_des_expanded_url = None
            retweet_origin_retweet_count = None

            origin_quoted = None
            quoted_time = None
            quoted_id = None
            quoted_origin_entities = None
            quoted_origin_urls = None
            quoted_origin_user = None
            quoted_origin_user_id = None
            quoted_origin_user_location = None
            quoted_origin_user_entities = None
            quoted_expanded_urls_array = None
            quoted_origin_user_intro_url = None
            quoted_origin_user_intro_urls = None
            quoted_origin_user_intro_expanded_url = None
            quoted_origin_user_description = None
            quoted_origin_user_des_urls = None
            quoted_origin_user_des_expanded_url = None
            quoted_origin_retweet_count = None

            obj = json.loads(line)

            retweeted_time = obj.get('created_at', None)  # 转帖时间
            retweeted_id = obj.get('id_str', None)  # 转贴id

            retweeted_user = obj.get('user', None)  # 转贴用户信息
            if retweeted_user:
                retweeted_user_id = retweeted_user.get('id_str', None)  # 转贴用户的id
                retweeted_user_location = retweeted_user.get('location', None)  # 转贴用户设置的位置

            # 转贴
            origin_retweet = obj.get('retweeted_status', None)  # 原贴信息
            if origin_retweet:
                retweet_time = origin_retweet.get('created_at', None)  # 原帖创建时间
                retweet_id = origin_retweet.get('id_str', None)  # 原帖id

                retweet_origin_entities = origin_retweet.get('entities', None)  # 原帖内容信息
                if retweet_origin_entities:
                    retweet_origin_urls = retweet_origin_entities.get('urls', None)  # 原帖中的urls
                    if retweet_origin_urls:
                        retweet_expanded_urls_array = []
                        for url_info in retweet_origin_urls:
                            expanded_url = url_info.get('expanded_url', None)
                            if expanded_url:
                                retweet_expanded_urls_array.append(expanded_url)

                retweet_origin_user = origin_retweet.get('user', None)  #原帖用户信息
                if retweet_origin_user:
                    retweet_origin_user_id = retweet_origin_user.get('id_str', None)
                    retweet_origin_user_location = retweet_origin_user.get('location', None)
                    retweet_origin_user_entities = retweet_origin_user.get('entities', None)

                    retweet_origin_user_intro_url = retweet_origin_user_entities.get('url', None)
                    if retweet_origin_user_intro_url:
                        retweet_origin_user_intro_urls = retweet_origin_user_intro_url.get('urls', None)
                        if retweet_origin_user_intro_urls and len(retweet_origin_user_intro_urls) > 0:
                            retweet_origin_user_intro_expanded_url = retweet_origin_user_intro_urls[0].get('expanded_url', None)
                        else:
                            retweet_origin_user_intro_expanded_url = None

                    retweet_origin_user_description = retweet_origin_user_entities.get('description', None)
                    if retweet_origin_user_description:
                        retweet_origin_user_des_urls = retweet_origin_user_description.get('urls', None)
                        if retweet_origin_user_des_urls and len(retweet_origin_user_des_urls) > 0:
                            retweet_origin_user_des_expanded_url = retweet_origin_user_des_urls[0].get('expanded_url', None)
                        else:
                            retweet_origin_user_des_expanded_url = None
                retweet_origin_retweet_count = origin_retweet.get('retweet_count', None)

            # 引用
            origin_quoted = obj.get('quoted_status', None)
            if origin_quoted:
                quoted_time = origin_quoted.get('created_at', None)
                quoted_id = origin_quoted.get('id_str', None)

                quoted_origin_entities = origin_quoted.get('entities', None)
                if quoted_origin_entities:
                    quoted_origin_urls = quoted_origin_entities.get('urls', None)
                    if quoted_origin_urls:
                        quoted_expanded_urls_array = []
                        for url_info in quoted_origin_urls:
                            expanded_url = url_info.get('expanded_url', None)
                            if expanded_url:
                                quoted_expanded_urls_array.append(expanded_url)

                quoted_origin_user = origin_quoted.get('user', None)  #原帖用户信息
                if quoted_origin_user:
                    quoted_origin_user_id = quoted_origin_user.get('id_str', None)
                    quoted_origin_user_location = quoted_origin_user.get('location', None)
                    quoted_origin_user_entities = quoted_origin_user.get('entities', None)

                    quoted_origin_user_intro_url = quoted_origin_user_entities.get('url', None)
                    if quoted_origin_user_intro_url:
                        quoted_origin_user_intro_urls = quoted_origin_user_intro_url.get('urls', None)
                        if quoted_origin_user_intro_urls and len(quoted_origin_user_intro_urls) > 0:
                            quoted_origin_user_intro_expanded_url = quoted_origin_user_intro_urls[0].get('expanded_url', None)
                        else:
                            quoted_origin_user_intro_expanded_url = None

                    quoted_origin_user_description = quoted_origin_user_entities.get('description', None)
                    if quoted_origin_user_description:
                        quoted_origin_user_des_urls = quoted_origin_user_description.get('urls', None)
                        if quoted_origin_user_des_urls and len(quoted_origin_user_des_urls) > 0:
                            quoted_origin_user_des_expanded_url = quoted_origin_user_des_urls[0].get('expanded_url', None)
                        else:
                            quoted_origin_user_des_expanded_url = None
                quoted_origin_retweet_count = origin_quoted.get('retweet_count', None)  # 原帖用户信息


            data_list.append(
                {'retweeted_time': retweeted_time,                                                  # 转帖时间
                 'retweeted_id': retweeted_id,                                                      # 转贴推文id
                 'retweeted_user_id': retweeted_user_id,                                            # 转贴用户id
                 'retweeted_user_location': retweeted_user_location,                                # 转贴用户位置

                 'retweet_time': retweet_time,                                                      # 被转贴的推文创建时间
                 'retweet_id': retweet_id,                                                          # 被转贴的推文id
                 'retweet_expanded_urls_array': retweet_expanded_urls_array,                        # 被转贴的推文中的url
                 'retweet_origin_user_id': retweet_origin_user_id,                                  # 被转贴的推文发布者id
                 'retweet_origin_user_location': retweet_origin_user_location,                      # 被转贴的推文发布者位置
                 'retweet_origin_user_intro_expanded_url': retweet_origin_user_intro_expanded_url,  # 被转贴的推文发布者设置中的url
                 'retweet_origin_user_des_expanded_url': retweet_origin_user_des_expanded_url,      # 被转贴的推文发布者描述中的url
                 'retweet_origin_retweet_count': retweet_origin_retweet_count,

                 'quoted_time': quoted_time,
                 'quoted_id': quoted_id,
                 'quoted_expanded_urls_array': quoted_expanded_urls_array,
                 'quoted_origin_user_id': quoted_origin_user_id,
                 'quoted_origin_user_location': quoted_origin_user_location,
                 'quoted_origin_user_intro_expanded_url': quoted_origin_user_intro_expanded_url,
                 'quoted_origin_user_des_expanded_url': quoted_origin_user_des_expanded_url,
                 'quoted_origin_retweet_count': quoted_origin_retweet_count
                })
            true_line += 1
    print("all line:", all_line, "\ttrue line:", true_line)
    df = pd.DataFrame(data_list, columns=[
        'retweeted_time', 'retweeted_id', 'retweeted_user_id', 'retweeted_user_location',
        'retweet_time', 'retweet_id', 'retweet_expanded_urls_array',
        'retweet_origin_user_id', 'retweet_origin_user_location',
        'retweet_origin_user_intro_expanded_url', 'retweet_origin_user_des_expanded_url', 'retweet_origin_retweet_count',
        'quoted_time', 'quoted_id', 'quoted_expanded_urls_array',
        'quoted_origin_user_id', 'quoted_origin_user_location',
        'quoted_origin_user_intro_expanded_url', 'quoted_origin_user_des_expanded_url', 'quoted_origin_retweet_count'
    ])
    df['retweet_expanded_urls_array'] = df['retweet_expanded_urls_array'].apply(
        lambda x: ', '.join(x) if isinstance(x, list) else x)
    df['quoted_expanded_urls_array'] = df['quoted_expanded_urls_array'].apply(
        lambda x: ', '.join(x) if isinstance(x, list) else x)

    # writer = pd.ExcelWriter(output_file, engine='openpyxl', mode='a')
    # df.to_excel(writer, index=False, header=False)
    # writer.save()

    # 使用 pd.ExcelWriter 打开 Excel 文件，如果不存在则创建
    try:
        writer = pd.ExcelWriter(output_file, engine='openpyxl', mode='a')
    except FileNotFoundError:
        # 如果文件不存在，使用 openpyxl 创建一个新的 Excel 文件
        wb = Workbook()
        wb.save(output_file)
        # 重新尝试打开 ExcelWriter
        writer = pd.ExcelWriter(output_file, engine='openpyxl', mode='a')

    # 在这里可以使用 writer 写入数据，比如使用 df.to_excel 方法
    df.to_excel(writer, index=False, header=False)
    writer._save()
    # 关闭 ExcelWriter 对象
    writer.close()



    print("finish:", input_file)
    return all_line, true_line


def batch_json_to_xlsx(num_file, num_txt, path_record):
    output_folder = f'H:\\republican\\republican-candidate-filter-ids-0{num_file}-output'
    # 检查文件夹是否存在
    if not os.path.exists(output_folder):
        # 如果不存在，创建文件夹
        os.makedirs(output_folder)
        print(f"Folder '{output_folder}' created.")
    else:
        print(f"Folder '{output_folder}' already exists.")

    for i in range(0, num_txt + 1):  # 生成0_output.xlsx-num_output.xslx
        input_txt_file = f"H:\\republican\\republican-candidate-filter-ids-0{num_file}\\republican-candidate-filter-ids-0{num_file}-ok-{i}.txt"
        output_xlsx_file = f"H:\\republican\\republican-candidate-filter-ids-0{num_file}-output\\republican-candidate-filter-ids-0{num_file}-ok-{i}-output.xlsx"
        print("-----------------------------------------------------------------------------------------------------")
        print(input_txt_file)
        print(output_xlsx_file)
        all_count, true_count = extract_txt_to_xlsx(input_txt_file, output_xlsx_file)
        # 记录提取结果
        with open(path_record, 'a', encoding='utf-8') as record_txt:
            print_string = f"republican-candidate-filter-ids-0{num_file}-ok-{i}总行数：{all_count}\t有效行数：{true_count}\t无效行数：{all_count - true_count}\n"
            record_txt.write(print_string)


if __name__ == "__main__":

    # file_num = 3  # 文件夹序号
    # file_in_num = 6  # 文件中ok的txt文件数量

    file_num = {
        # 4: 15,
        # 5: 15,
        # 6: 14,
        # 7: 15,
        # 8: 15,
        # 9: 15,
        # 10: 15,
        # 11: 15,
        # 12: 15,
        # 13: 15,
        # 14: 15,
        # 15: 15,
        # 16: 14,
        # 17: 15,

        3: 11,
        4: 11,
        5: 10,
        6: 17,
    }

    for i in range(3, 7):

        # 记录过程中的结果
        record_data_path = f'H:\\republican\\republican-candidate-filter-ids-0{i}-txt-data.txt'
        if not os.path.isfile(record_data_path):
            # 如果文件不存在，创建文件
            with open(record_data_path, 'w') as file:
                print(f"文件 '{record_data_path}' 不存在，已创建。")
                # 在文件中写入数据或执行其他操作

        batch_json_to_xlsx(i, file_num[i], record_data_path)

        # input__file = f"H:\\demo.txt"
        # output__file = f"H:\\demo.xlsx"
        # all_count, true_count = extract_txt_to_xlsx(input__file, output__file)
        # print(all_count, true_count)

        print("完成数据的提取!")

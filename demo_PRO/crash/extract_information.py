import json
import pandas as pd
import os
import tempfile
import shutil
from openpyxl.utils.exceptions import IllegalCharacterError



def check_json_brackets(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        line_number = 0
        error_count = 0

        for line in file:
            line_number += 1
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                # 如果捕获到 JSONDecodeError，说明 JSON 数据格式有问题
                print(f"行号 {line_number}: {line.strip()} 不是有效的 JSON 数据。")
                error_count += 1

        return error_count

def check_and_remove_invalid_lines(file_path):

    temp_file_path = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8').name
    temp_dir = tempfile.gettempdir()
    print(temp_dir)

    line_number = 0
    true_count = 0
    error_count = 0
    kong_count = 0
    has_error = False

    with open(file_path, 'r', encoding='utf-8') as source_file, open(temp_file_path, 'w', encoding='utf-8') as temp_file:
        for line in source_file:
            line_number += 1
            try:
                json.loads(line)
                temp_file.write(line)
                true_count += 1
            except json.JSONDecodeError as e:
                # 如果捕获到 JSONDecodeError，说明 JSON 数据格式有问题
                print(f"行号 {line_number}: {line.strip()} \n 不是有效的 JSON 数据。")
                with open("H:\\democratic\\line_error.txt", 'a', encoding='utf-8') as error_file:
                    error_file.write(line.strip() + '\n')
                error_count += 1
                has_error = True
            except Exception as e:
                # 捕获其他异常，如果是空行则删除
                if not line.strip():
                    print(f"行号 {line_number}: 空行。已删除。")
                    kong_count += 1
                    continue
                else:
                    print(f"行号 {line_number}: {line.strip()} \n 其他异常: {e}")
                    has_error = True

    if has_error:
        shutil.move(temp_file_path, file_path)  # 将临时文件替换原始文件
        print(f"未错误的行数：{true_count}")
        print(f"已删除错误行，发生错误的行数：{error_count}")
        print(f"已删除空行，发生错误的行数：{kong_count}")
        return true_count, error_count, kong_count
    else:
        print("所有行的 JSON 数据格式都是完整的，未修改文件。")
        temp_file.close()
        os.remove(temp_file_path)
        return true_count, error_count, kong_count  # 表示没有错误

def split_text_file(input_file_path, output_folder, count, file_num, path_record, lines_per_file=500000):

    # 打开输入文件
    with open(input_file_path, 'r', encoding='utf-8') as input_file:

        print("-----------------------------------------------------------------------------------------------------")
        print("open input_txt:", input_file_path)

        # 创建输出文件夹（如果不存在）
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 行数计数
        lines_written = 0
        output_file_path = os.path.join(output_folder, f'democratic-candidate-filter-ids-{file_num}-ok-{count}.txt')


        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            print("open output_txt:", output_file_path )
            for line in input_file:
                output_file.write(line)
                lines_written += 1

                if not line.strip():
                    # 如果当前行是空行，说明拆分完成，结束程序

                    break

                if lines_written >= lines_per_file:
                    # 如果已经写入的行数达到了 lines_per_file，打开下一个文件
                    print("close:", output_file_path)
                    print(lines_written)
                    output_file.close()
                    with open(path_record, 'a', encoding='utf-8') as record_txt:
                        print_string = f"democratic-candidate-filter-ids-{file_num}-ok-{count}的行数：{lines_written}\n"
                        record_txt.write(print_string)
                    lines_written = 0


                    count += 1
                    output_file_path = os.path.join(output_folder, f'democratic-candidate-filter-ids-{file_num}-ok-{count}.txt')
                    output_file = open(output_file_path, 'w', encoding='utf-8')
                    print("open output_txt:", output_file_path)

        print("close:", output_file_path)
        print(lines_written)
        output_file.close()
        with open(path_record, 'a', encoding='utf-8') as record_txt:
            print_string = f"democratic-candidate-filter-ids-{file_num}-ok-{count}的行数：{lines_written}\n"
            record_txt.write(print_string)

    return count+1

def extract_txt_to_xlsx(input_file, output_file, path_record):
    data_list = []  # 创建一个空的data_list列表，用于存储从txt文件中提取的数据
    all_line = 0
    true_line = 0
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            all_line += 1
            obj = json.loads(line)
            current_twitter_id_str = obj.get('id_str', None)
            c_value = obj.get('created_at', None)
            user = obj.get('user', {})
            current_user_id_str = user.get('id_str', None)
            referenced_tweets = obj.get('retweeted_status', {})
            origin_twitter_id = referenced_tweets.get('id_str', None)
            origin_user = referenced_tweets.get('user', {})
            origin_user_id = origin_user.get('id_str', None)
            origin_user_entities = origin_user.get('entities', None)
            current_twitter_retweet_count = obj.get('retweet_count', None)
            origin_twitter_retweet_count = referenced_tweets.get('retweet_count', None)
            current_user_location = user.get('location', None)
            origin_user_location = origin_user.get('location', None)
            current_user_screen_name = user.get('screen_name', None)
            origin_user_screen_name = origin_user.get('screen_name', None)

            # print("1", current_twitter_id_str, "\t2", c_value, "\t3", user, "\n4", current_user_id_str, "\t5",
            #       referenced_tweets, "\t6", origin_twitter_id, "\t7", origin_user, "\t8", origin_user_id, )


            myurl = ""
            expanded_url = ""
            display_url = ""
            if origin_user_entities:
                entities_url = origin_user_entities.get('url', None)
                if entities_url:
                    urls = entities_url.get('urls', [])
                    if urls:
                        for url_obj in urls:
                            # print("entities.url.urls:", urls)
                            myurl = url_obj.get('url', None)
                            expanded_url = url_obj.get('expanded_url', None)
                            display_url = url_obj.get('display_url', None)
                            # print("1.url:", myurl, "2.expanded_url:", display_url, "3.display_url", display_url)
            if any((current_user_id_str, current_twitter_id_str, origin_user_id, origin_twitter_id,
                    c_value,myurl,expanded_url,display_url,current_twitter_retweet_count,origin_twitter_retweet_count,current_user_location,origin_user_location,current_user_screen_name,origin_user_screen_name)):  # 如果这些字段都不是全部为空值才可以添加
                data_list.append(
                    {'current_user_id_str': current_user_id_str, 'current_twitter_id_str': current_twitter_id_str,
                     'origin_user_id': origin_user_id, 'origin_twitter_id': origin_twitter_id, 'created_at': c_value, 'url': myurl, 'expanded_url': expanded_url, 'display_url': display_url,
                     'current_twitter_retweet_count': current_twitter_retweet_count, 'origin_twitter_retweet_count':origin_twitter_retweet_count,
                     'current_user_location':current_user_location, 'origin_user_location':origin_user_location, 'current_user_screen_name':current_user_screen_name,'origin_user_screen_name': origin_user_screen_name})
                true_line += 1
    print("all line:", all_line, "\ttrue line:", true_line)

    slect = True
    #slect = False

    if slect:
        # 没有无法输入字符
        df = pd.DataFrame(data_list,
                          columns=['current_user_id_str', 'current_twitter_id_str', 'origin_user_id', 'origin_twitter_id',
                                   'created_at', 'url', 'expanded_url', 'display_url', 'current_twitter_retweet_count', 'origin_twitter_retweet_count', 'current_user_location', 'origin_user_location','current_user_screen_name', 'origin_user_screen_name'])
        writer = pd.ExcelWriter(output_file, engine='openpyxl')
        df.to_excel(writer, index=False, header=False)
        writer._save()
    else:
        # 错误字符检测行数`
        try:
            df = pd.DataFrame(data_list,
                              columns=['current_user_id_str', 'current_twitter_id_str', 'origin_user_id',
                                       'origin_twitter_id',
                                       'created_at', 'url', 'expanded_url', 'display_url', 'current_twitter_retweet_count',
                                       'origin_twitter_retweet_count', 'current_user_location', 'origin_user_location',
                                       'current_user_screen_name', 'origin_user_screen_name'])
            writer = pd.ExcelWriter(output_file, engine='openpyxl')
            for index, row in df.iterrows():
                try:
                    row.to_frame().T.to_excel(writer, startrow=index, index=False, header=False)
                except IllegalCharacterError as e:
                    print(f"第 {index + 1} 行数据包含不可写入字符: {row}")
            writer.save()
            print("数据已成功写入 Excel 文件")
        except IllegalCharacterError as e:
            print(f"写入 Excel 文件时发生不可写入字符错误: {e}")


    print("finish:", input_file)
    return all_line, true_line

#   批量处理生成数据
def batch_json_to_xlsx(num_file, num_txt, path_record):

    output_folder = f'H:\\democratic\\democratic-candidate-filter-ids-{num_file}-output'
    # 检查文件夹是否存在
    if not os.path.exists(output_folder):
        # 如果不存在，创建文件夹
        os.makedirs(output_folder)
        print(f"Folder '{output_folder}' created.")
    else:
        print(f"Folder '{output_folder}' already exists.")

    for i in range(6, num_txt + 1):  # 生成0_output.xlsx-num_output.xslx
        input_txt_file = f"H:\\democratic\\democratic-candidate-filter-ids-{num_file}\\democratic-candidate-filter-ids-{num_file}-ok-{i}.txt"
        output_xlsx_file = f"H:\\democratic\\democratic-candidate-filter-ids-{num_file}-output\\democratic-candidate-filter-ids-{num_file}-ok-{i}-output.xlsx"
        print("-----------------------------------------------------------------------------------------------------")
        print(input_txt_file)
        print(output_xlsx_file)
        all_count, true_count = extract_txt_to_xlsx(input_txt_file, output_xlsx_file, path_record)
        with open(path_record, 'a', encoding='utf-8') as record_txt:
            print_string = f"democratic-candidate-filter-ids-{num_file}-ok-{i}总行数：{all_count}\t有效行数：{true_count}\t无效行数：{all_count - true_count}\n"
            record_txt.write(print_string)


#   批量拆分txt
def batch_split_text(num_file, num_txt, path_record):

    input_folder = f'H:\\democratic\\democratic-candidate-filter-ids-{num_file}'  # 替换为你的输入文件的文件夹路径
    output_folder = f'H:\\democratic\\democratic-candidate-filter-ids-{num_file}'  # 替换为你想要保存拆分文件的文件夹路径
    file_count = 0

    for i in range(1, num_txt+1):
        input_file_path = os.path.join(input_folder, f'democratic-candidate-filter-ids-{num_file}_0{i}-ok.txt')
        file_count = split_text_file(input_file_path, output_folder, file_count, num_file, path_record)
    return file_count
#   批量处理检测json错误
def batch_check_json(num_file, num_txt, path_record):

    for i in range(1, num_txt+1):
        print("-------------------------------------------------------------------------------------------------------")
        input_txt_file = f'H:\\democratic\\democratic-candidate-filter-ids-{num_file}\\democratic-candidate-filter-ids-{num_file}_0{i}-ok.txt'
        print("check:", input_txt_file)
        # error_count = check_json_brackets(input_txt_file)
        true_count, error_count, kong_count = check_and_remove_invalid_lines(input_txt_file)

        with open(path_record, 'a', encoding='utf-8') as record_txt:
            print_string = f"democratic-candidate-filter-ids-{num_file}_0{i}-ok 正确行数：{true_count}\t错误行数：{error_count}\t空行数：{kong_count}\n"
            record_txt.write(print_string)




if __name__ == "__main__":

    file_num = 17            #文件夹序号
    file_in_num = 6        #文件中ok的txt文件数量

    # 记录过程中的结果
    record_data_path = f'H:\\democratic\\democratic-candidate-filter-ids-{file_num}-txt-data.txt'
    if not os.path.isfile(record_data_path):
        # 如果文件不存在，创建文件
        with open(record_data_path, 'w') as file:
            print(f"文件 '{record_data_path}' 不存在，已创建。")
            # 在文件中写入数据或执行其他操作


    #检查json是否有错误并处理
    # batch_check_json(file_num, file_in_num, record_data_path)
    # print("完成错误检查和处理!")
    # # 批量拆分大型txt文件
    # txt_num = batch_split_text(file_num, file_in_num,record_data_path)
    # print("完成拆分！")
    # #批量生成n_output.xlsx
    batch_json_to_xlsx(file_num, 15, record_data_path)
    print("完成数据的提取!")




import json
import os
import shutil
import tempfile


# 删除文件夹中以'-bad.txt'结尾的txt
def delete_bad_txt(directory, record_path):
    for filename in os.listdir(directory):
        # 检查文件名是否以 '-bad.txt' 结尾
        if filename.endswith("-bad.txt"):
            # 构建文件的完整路径
            file_path = os.path.join(directory, filename)
            # 删除文件
            os.remove(file_path)
            with open(record_path, 'a', encoding='utf-8') as f_delete:
                f_delete.write(f"Deleted: {file_path}\n")
            print(f"Deleted: {file_path}")


def check_and_remove_invalid_lines(txt_source_path, error_record_path):
    temp_file_path = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8').name
    temp_dir = tempfile.gettempdir()
    print("Temporary file path:", temp_dir)

    line_number = 0
    true_count = 0
    error_count = 0
    null_count = 0
    has_error = False

    with (open(txt_source_path, 'r', encoding='utf-8') as source_file,
          open(temp_file_path, 'w', encoding='utf-8') as temp_file,
          open(error_record_path, 'a', encoding='utf-8') as error_file):
        for line in source_file:
            line_number += 1
            try:
                json.loads(line)
                temp_file.write(line)
                true_count += 1
            except json.JSONDecodeError:
                # 如果捕获到 JSONDecodeError，说明 JSON 数据格式有问题
                print(f"行号 {line_number}: {line.strip()} \n 不是有效的 JSON 数据。")
                error_file.write(line.strip() + '\n')
                error_count += 1
                has_error = True
            except Exception as e:
                # 捕获其他异常，如果是空行则删除
                if not line.strip():
                    print(f"行号 {line_number}: 空行。已删除。")
                    null_count += 1
                    continue
                else:
                    print(f"行号 {line_number}: {line.strip()} \n 其他异常: {e}")
                    has_error = True

    if has_error:
        shutil.move(temp_file_path, txt_source_path)  # 将临时文件替换原始文件
        print(f"未错误的行数：{true_count}")
        print(f"已删除错误行，发生错误的行数：{error_count}")
        print(f"已删除空行，发生错误的行数：{null_count}")

    else:
        print("所有行的 JSON 数据格式都是完整的，未修改文件。")
        temp_file.close()
        os.remove(temp_file_path)

    return true_count, error_count, null_count


def batch_check_and_remove_invalid_lines(source_txt_directory, record_json_path, error_txt_path):
    for filename in os.listdir(source_txt_directory):
        print(
            "-----------------------------------------------------------------------------------------------------------")
        print(filename)
        true_count, error_count, null_count = check_and_remove_invalid_lines(
            os.path.join(source_txt_directory, filename), error_txt_path)
        print(f"正确行数：{true_count}\t错误行数：{error_count}\t空行数：{null_count}\n")

        with open(record_json_path, 'a', encoding='utf-8') as f_batch_check:
            f_batch_check.write(f"{filename}: 正确行数：{true_count}\t\t错误行数：{error_count}\t\t空行数：{null_count}\n")


def merge_source_json_line(source_txt_directory_path, merge_txt_directory_path, record_txt_path_merge):
    # 准备一个字典来按日期组织文件
    files_by_date = {}

    # 遍历目录中的文件
    for filename in os.listdir(source_txt_directory_path):
        if filename.startswith('us-presidential-tweet-id') and filename.endswith('ok.txt'):
            # 从文件名解析日期
            date = '-'.join(filename.split('-')[4:7])
            if date not in files_by_date:
                files_by_date[date] = []
            files_by_date[date].append(filename)

    for key, value in files_by_date.items():
        print(f"{key}: ", end='')
        for i, filename in enumerate(value, 1):
            end_char = '\n\t\t\t' if i % 3 == 0 else ', '
            print(filename, end=end_char)
        print()
    with open(record_txt_path_merge, 'a', encoding='utf-8') as f_merge_01:
        for key, value in files_by_date.items():
            f_merge_01.write(f"{key}: ")
            for i, filename in enumerate(value, 1):
                end_char = '\n\t\t   ' if i % 3 == 0 else ', '
                f_merge_01.write(f"{filename}{end_char}")
            f_merge_01.write("\n")

    # 按日期处理文件
    for date, filenames in files_by_date.items():
        # 按文件名排序以确保顺序
        sorted_filenames = sorted(filenames)
        lines_written = 0
        file_counter = 1
        output_file = None

        for filename in sorted_filenames:
            being_processed_txt = os.path.join(source_txt_directory_path, filename)
            print(f"being_processed:  {being_processed_txt}")
            with open(being_processed_txt, 'r', encoding='utf-8') as f:
                for line in f:
                    # 如果当前文件行数达到五十万，或者是处理的第一行，打开一个新文件
                    if lines_written == 500000 or lines_written == 0:
                        if output_file:
                            output_file.close()
                            print(
                                "--------------------------------------------------------------------------------------------")
                            print(f"close merge txt: {output_filename}\tnum_line: {lines_written}")
                            with open(record_txt_path_merge, 'a', encoding='utf-8') as f_merge_02:
                                f_merge_02.write(f"merge txt: {output_filename}\tnum_line: {lines_written}\n")
                            print(
                                "--------------------------------------------------------------------------------------------")
                        output_filename = f"{date}-{file_counter}-merged-ok.txt"
                        print(
                            "--------------------------------------------------------------------------------------------")
                        print(f"create merge txt: {output_filename}")
                        print(
                            "--------------------------------------------------------------------------------------------")

                        output_file = open(os.path.join(merge_txt_directory_path, output_filename), 'w', encoding='utf-8')
                        file_counter += 1
                        lines_written = 0
                    output_file.write(line)
                    lines_written += 1
            print(f"close source txt: {being_processed_txt}")

        if output_file:
            output_file.close()
            print("--------------------------------------------------------------------------------------------")
            print(f"close merge txt: {output_filename}\tnum_line: {lines_written}")
            with open(record_txt_path_merge, 'a', encoding='utf-8') as f_merge_02:
                f_merge_02.write(f"merge txt: {output_filename}\tnum_line: {lines_written}\n")
            print("--------------------------------------------------------------------------------------------")


def wash_json(record_txt_path, merge_directory_path, source_directory_path, error_json_path):
    print("Deleted:'-bad.txt'")
    print("-----------------------------------------------------------------------------------------------------------")
    with open(record_txt_path, 'a', encoding='utf-8') as file:
        file.write(f"Deleted:'-bad.txt'\n")
    delete_bad_txt(source_directory_path, record_txt_path)

    print("===========================================================================================================")
    with open(record_txt_path, 'a', encoding='utf-8') as file:
        file.write(
            f"-----------------------------------------------------------------------------------------------------------\n")

    print("check_and_remove_invalid_json")
    with open(record_txt_path, 'a', encoding='utf-8') as file:
        file.write(f"check_and_remove_invalid_json:\n")
    batch_check_and_remove_invalid_lines(source_directory_path, record_txt_path, error_json_path)

    print("===========================================================================================================")
    with open(record_txt_path, 'a', encoding='utf-8') as file:
        file.write(
            f"-----------------------------------------------------------------------------------------------------------\n")

    print("Merge same date txt")
    print("-----------------------------------------------------------------------------------------------------------")
    with open(record_txt_path, 'a', encoding='utf-8') as file:
        file.write(f"Merge same date txt:\n")
    merge_source_json_line(source_directory_path, merge_directory_path, record_txt_path)


if __name__ == "__main__":

    # wash_json("H:\\record_2020_09.txt", "H:\\merge_2020_09",
    #           "H:\\2020-09", "H:\\error_json_2020-09.txt")
    #
    # # merge_source_json_line("H:\\2020-09", "H:\\merge_2020_09", "H:\\record_2020_09.txt")
    #
    # wash_json("H:\\record_2020_10.txt", "H:\\merge_2020_10",
    #           "H:\\2020-10", "H:\\error_json_2020-10.txt")
    #
    # wash_json("H:\\record_2020_11.txt", "H:\\merge_2020_11",
    #           "H:\\2020-11", "H:\\error_json_2020_11.txt")
    #
    # wash_json("H:\\record_2020_12.txt", "H:\\merge_2020_12",
    #           "H:\\2020-12", "H:\\error_json_2020_12.txt")

    # wash_json("H:\\record_2021_01.txt", "H:\\merge_2021_01",
    #           "H:\\2021-01", "H:\\error_json_2021_01.txt")
    #
    # wash_json("H:\\record_2021_02.txt", "H:\\merge_2021_02",
    #           "H:\\2021-02", "H:\\error_json_2021_02.txt")

    # wash_json("H:\\record_2019_12.txt", "H:\\merge_2019_12",
    #           "H:\\2019-12", "H:\\error_json_2019_12.txt")
    # wash_json("H:\\record_2020_01.txt", "H:\\merge_2020_01",
    #           "H:\\2020-01", "H:\\error_json_2020_01.txt")

    # wash_json("H:\\record_2020_02.txt", "H:\\merge_2020_02",
    #           "H:\\2020-02", "H:\\error_json_2020_02.txt")
    # wash_json("H:\\record_2020_03.txt", "H:\\merge_2020_03",
    #           "H:\\2020-03", "H:\\error_json_2020_03.txt")
    # wash_json("H:\\record_2020_04.txt", "H:\\merge_2020_04",
    #           "H:\\2020-04", "H:\\error_json_2020_04.txt")
    #
    # wash_json("H:\\record_2020_05.txt", "H:\\merge_2020_05",
    #           "H:\\2020-05", "H:\\error_json_2020_05.txt")
    # wash_json("H:\\record_2020_06.txt", "H:\\merge_2020_06",
    #           "H:\\2020-06", "H:\\error_json_2020_06.txt")
    # wash_json("H:\\record_2020_07.txt", "H:\\merge_2020_07",
    #           "H:\\2020-07", "H:\\error_json_2020_07.txt")
    wash_json("H:\\record_2020_08.txt", "H:\\merge_2020_08",
              "H:\\2020-08", "H:\\error_json_2020_08.txt")





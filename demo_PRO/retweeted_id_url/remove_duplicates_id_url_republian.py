# 去除重复的映射关系：被转发推文id ↔ url

import os
import pandas as pd


def remove_duplicates_id_url(old_xlsx_path, new_xlsx_path):
    print(f"内容开始读取!")
    df = pd.read_excel(old_xlsx_path, sheet_name="Sheet1", header=0, dtype=str)
    print(f"内容读取成功!")
    # print(df)
    line_num_remove_before = df.shape[0]

    df_unique = df.drop_duplicates(subset=['ID', 'URL'], keep='first')
    df_unique.reset_index(drop=True, inplace=True)
    # print(df_unique)
    line_num_remove_after = df_unique.shape[0]

    df_unique.to_excel(new_xlsx_path, index=False)

    return line_num_remove_before, line_num_remove_after


def batch_remove_dup(num_file, num_xlsx):
    record_txt = f'H:\\retweeted_id - url\\republican_remove_dup\\{num_file}\\{num_file}.txt'

    for i in range(0, num_xlsx + 1):  # 生成0_output.xlsx-num_output.xslx
        input_xlsx = f'H:\\retweeted_id - url\\republican\\{num_file}\\{num_file}-{i}.xlsx'
        output_xlsx = f'H:\\retweeted_id - url\\republican_remove_dup\\{num_file}\\{num_file}-{i}.xlsx'
        print("-----------------------------------------------------------------------------------------------------")
        print(input_xlsx)
        print(output_xlsx)
        print(record_txt)
        line_num_remove_before, line_num_remove_after = remove_duplicates_id_url(input_xlsx, output_xlsx, )

        with open(record_txt, 'a', encoding='utf-8') as rt:
            print_string = f"republican-{num_file}-{i}：line_num_remove_before: {line_num_remove_before}\t\tline_num_remove_after: {line_num_remove_after}\n"
            rt.write(print_string)

if __name__ == "__main__":
    # remove_duplicates_id_url("H:\\demo_remove.xlsx", "H:\\demo_remove_dup_id_url.xlsx")

    file_num = {
        3: 11,
        4: 11,
        5: 10,
        6: 17,
    }

    for i in range(3, 7):

        print("=====================================================================================================")
        output_folder = f'H:\\retweeted_id - url\\republican_remove_dup\\{i}'
        # 检查文件夹是否存在
        if not os.path.exists(output_folder):
            # 如果不存在，创建文件夹
            os.makedirs(output_folder)
            print(f"Folder '{output_folder}' created.")
        else:
            print(f"Folder '{output_folder}' already exists.")

        batch_remove_dup(i, file_num[i])

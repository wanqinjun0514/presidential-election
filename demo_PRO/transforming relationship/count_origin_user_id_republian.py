import os

import numpy as np
import pandas as pd


def count_user_id(xlsx_path, result_path):
    print(f"内容开始读取!")
    df = pd.read_excel(xlsx_path, sheet_name="Sheet1", header=0, dtype=str)
    print(f"内容读取成功!")

    line_num_before = 0
    line_num_after = 0

    pd.set_option('expand_frame_repr', False)
    # print(df)
    line_num_before = df.shape[0]

    selected_values = df.iloc[:, [3]].values
    np.set_printoptions(linewidth=500)
    # print(selected_values)

    value_counts = np.unique(selected_values, return_counts=True)
    # print(value_counts)

    result_df = pd.DataFrame({
        'Value': value_counts[0],
        'Count': value_counts[1]
    })

    # print(result_df)

    result_df = result_df.sort_values(by='Count', ascending=False)
    # print(result_df)
    line_num_after = result_df.shape[0]

    result_df.to_excel(result_path, index=False, header=True)

    return line_num_before, line_num_after


def batch_extract_relationship(num_file, num_xlsx):
    record_txt = f'H:\\tranforming_relationship\\republican_count\\{num_file}\\{num_file}.txt'

    for i in range(0, num_xlsx + 1):  # 生成0_output.xlsx-num_output.xslx
        input_xlsx = f"H:\\tranforming_relationship\\republican\\{num_file}\\{num_file}-{i}.xlsx"
        output_xlsx = f'H:\\tranforming_relationship\\republican_count\\{num_file}\\{num_file}-{i}.xlsx'
        print("-----------------------------------------------------------------------------------------------------")
        print(input_xlsx)
        print(output_xlsx)
        print(record_txt)
        line_num_before, line_num_after = count_user_id(input_xlsx, output_xlsx, )

        with open(record_txt, 'a', encoding='utf-8') as rt:
            print_string = f"republican-{num_file}-{i}：line_num_before: {line_num_before}\t\tline_num_after: {line_num_after}\n"
            rt.write(print_string)


if __name__ == "__main__":

    # count_user_id("H:\\demo\\demo_count_userid.xlsx", "H:\\demo\\result_count_userid.xlsx")

    file_num = {
        3: 11,
        4: 11,
        5: 10,
        6: 17,
    }

    for i in range(3, 7):  # 文件名字

        print("=====================================================================================================")
        output_folder = f'H:\\tranforming_relationship\\republican_count\\{i}'
        # 检查文件夹是否存在
        if not os.path.exists(output_folder):
            # 如果不存在，创建文件夹
            os.makedirs(output_folder)
            print(f"Folder '{output_folder}' created.")
        else:
            print(f"Folder '{output_folder}' already exists.")

        batch_extract_relationship(i, file_num[i])

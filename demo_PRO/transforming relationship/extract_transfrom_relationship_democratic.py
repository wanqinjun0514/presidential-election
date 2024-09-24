import os
import pandas as pd
import numpy as np


def extract_relationship(xlsx_path, result_path):
    print(f"内容开始读取!")
    df = pd.read_excel(xlsx_path, sheet_name="Sheet1", header=None, dtype=str)
    print(f"内容读取成功!")

    pd.set_option('expand_frame_repr', False)

    selected_values = df.iloc[:, [1, 2, 5, 6, 7, 13, 14, 15]].values
    # selected_values = df.iloc[:, [1, 2, 5, 6, 7]].values
    line_num = selected_values.shape[0]
    np.set_printoptions(linewidth=500)
    # print(selected_values)
    # print(line_num)

    result_array = []
    count = 0

    for i in range(0, line_num):
        if i % 50000 == 0:  # 当i是50000的倍数时
            print(f"行数: {i}")

        if (pd.notna(selected_values[i, 2]) and pd.isna(selected_values[i, 3])) or (
                pd.notna(selected_values[i, 5]) and pd.isna(selected_values[i, 6])):
            # print(selected_values[i])
            count += 1
            if pd.notna(selected_values[i, 2]) and pd.isna(selected_values[i, 3]):
                new_row = [selected_values[i, 0],  # 第1列
                           selected_values[i, 1],  # 第2列
                           selected_values[i, 2],  # 第3列
                           selected_values[i, 4], ]  # 第4列
                result_array.append(new_row)
            elif pd.notna(selected_values[i, 5]) and pd.isna(selected_values[i, 6]):
                new_row = [selected_values[i, 0],  # 第1列
                           selected_values[i, 1],  # 第2列
                           selected_values[i, 5],  # 第3列
                           selected_values[i, 7], ]  # 第4列
                result_array.append(new_row)

    # for i in range(0, line_num):
    #     if i % 50000 == 0:  # 当i是50000的倍数时
    #         print(f"行数: {i}")
    #
    #     if pd.notna(selected_values[i, 2]) and pd.isna(selected_values[i, 3]):
    #         # print(selected_values[i])
    #         count += 1
    #         new_row = [selected_values[i, 0],  # 第1列
    #                    selected_values[i, 1],  # 第2列
    #                    selected_values[i, 2],  # 第3列
    #                    selected_values[i, 4], ]  # 第4列
    #         result_array.append(new_row)

    # print(result_array)

    # 将数组转换为 DataFrame
    df_result = pd.DataFrame(result_array, columns=['retweeted_id', 'retweeted_user_id', 'retweet_id', 'retweet_origin_user_id'])
    # print(df_result)

    # 存储 DataFrame 到 Excel 文件中
    df_result.to_excel(result_path, index=False, header=True)

    return count, line_num


def batch_extract_relationship(num_file, num_xlsx):
    record_txt = f'H:\\tranforming_relationship\\democratic\\{num_file}\\{num_file}.txt'

    for i in range(3, num_xlsx + 1):  # 生成0_output.xlsx-num_output.xslx
        input_xlsx = f"H:\\democratic\\democratic-candidate-filter-ids-{num_file}-output\\democratic-candidate-filter-ids-{num_file}-ok-{i}-output.xlsx"
        output_xlsx = f'H:\\tranforming_relationship\\democratic\\{num_file}\\{num_file}-{i}.xlsx'
        print("-----------------------------------------------------------------------------------------------------")
        print(input_xlsx)
        print(output_xlsx)
        print(record_txt)
        count, line_num = extract_relationship(input_xlsx, output_xlsx, )

        with open(record_txt, 'a', encoding='utf-8') as rt:
            print_string = f"democratic-{num_file}-{i}：count: {count}\t\tline_num: {line_num}\n"
            rt.write(print_string)


if __name__ == "__main__":
    # extract_relationship("H:\\demo\\demo_split_output.xlsx", "H:\\demo\\result_split_output.xlsx")

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

    for i in range(17, 18):         # 文件名字

        print("=====================================================================================================")
        output_folder = f'H:\\tranforming_relationship\\democratic\\{i}'
        # 检查文件夹是否存在
        if not os.path.exists(output_folder):
            # 如果不存在，创建文件夹
            os.makedirs(output_folder)
            print(f"Folder '{output_folder}' created.")
        else:
            print(f"Folder '{output_folder}' already exists.")

        batch_extract_relationship(i, file_num[i])


# 8-15、9-15、10-15
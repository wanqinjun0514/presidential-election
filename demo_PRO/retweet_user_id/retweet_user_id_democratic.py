import os
import pandas as pd
import numpy as np


def extract_user_id(xlsx_path, result_path):
    print(f"内容开始读取!")
    df = pd.read_excel(xlsx_path, sheet_name="Sheet1", header=None, dtype=str)
    print(f"内容读取成功!")

    pd.set_option('expand_frame_repr', False)
    # print(df)

    selected_values = df.iloc[:, [2, 3, ]].values
    line_num = selected_values.shape[0]
    np.set_printoptions(linewidth=500)

    # for i in range(0, line_num):
    #     print(selected_values[i])

    df_result = pd.DataFrame(selected_values, columns=['retweet_id', 'localation'])

    df_result.to_excel(result_path, index=False, header=True)

    return line_num


def batch_extract_relationship(num_file, num_xlsx):
    record_txt = f'H:\\retweet_user_id\\democratic\\{num_file}\\{num_file}.txt'

    for j in range(0, num_xlsx + 1):  # 生成0_output.xlsx-num_output.xslx
        input_xlsx = f"H:\\democratic\\democratic-candidate-filter-ids-{num_file}-output\\democratic-candidate-filter-ids-{num_file}-ok-{j}-output.xlsx"
        output_xlsx = f'H:\\retweet_user_id\\democratic\\{num_file}\\{num_file}-{j}.xlsx'
        print("-----------------------------------------------------------------------------------------------------")
        print(input_xlsx)
        print(output_xlsx)
        print(record_txt)
        line_num = extract_user_id(input_xlsx, output_xlsx, )

        with open(record_txt, 'a', encoding='utf-8') as rt:
            print_string = f"democratic-{num_file}-{j}：line_num: {line_num}\n"
            rt.write(print_string)


if __name__ == "__main__":
    # extract_user_id("H:\\demo\\demo_split_output.xlsx", "H:\\demo\\result_user_id_output.xlsx")

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

    for i in range(14, 18):  # 文件名字

        print("=====================================================================================================")
        output_folder = f'H:\\retweet_user_id\\democratic\\{i}'
        # 检查文件夹是否存在
        if not os.path.exists(output_folder):
            # 如果不存在，创建文件夹
            os.makedirs(output_folder)
            print(f"Folder '{output_folder}' created.")
        else:
            print(f"Folder '{output_folder}' already exists.")

        batch_extract_relationship(i, file_num[i])


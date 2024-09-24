import os
import pandas as pd


def split_output(xlsx_path, result_path_exist_url, result_path_without_url, result_path_no_retweeted):
    print(f"内容开始读取!")
    df = pd.read_excel(xlsx_path, sheet_name="Sheet1", header=None, dtype=str)
    print(f"内容读取成功!")
    # pd.set_option('expand_frame_repr', False)
    # print(df)

    count_exist_url = 0
    count_without_url = 0
    count_no_retweeted = 0
    df_exist_url = pd.DataFrame()
    df_without_url = pd.DataFrame()
    df_no_retweeted = pd.DataFrame()
    i = 0

    for index, row in df.iterrows():
        # if i % 50000 == 0:  # 当i是50000的倍数时
        print(f"行数: {i}")
        i += 1
        if pd.isna(row[5]) and pd.isna(row[13]):
            df_no_retweeted = df_no_retweeted._append(row, ignore_index=True)
            count_no_retweeted += 1
        elif pd.notna(row[5]):
            if pd.isna(row[6]):
                df_without_url = df_without_url._append(row, ignore_index=True)
                count_without_url += 1
            else:
                df_exist_url = df_exist_url._append(row, ignore_index=True)
                count_exist_url += 1
        elif pd.notna(row[13]):
            if pd.isna(row[14]):
                df_without_url = df_without_url._append(row, ignore_index=True)
                count_without_url += 1
            else:
                df_exist_url = df_exist_url._append(row, ignore_index=True)
                count_exist_url += 1

    # print("-----------------------------------------------------------------------------------------------------")
    # print(count_exist_url)
    # print(df_exist_url)
    # print("-----------------------------------------------------------------------------------------------------")
    # print(count_without_url)
    # print(df_without_url)
    # print("-----------------------------------------------------------------------------------------------------")
    # print(count_no_retweeted)
    # print(df_no_retweeted)

    df_exist_url.to_excel(result_path_exist_url, header=False, index=False)
    df_without_url.to_excel(result_path_without_url, header=False, index=False)
    df_no_retweeted.to_excel(result_path_no_retweeted, header=False, index=False)

    return count_exist_url, count_without_url, count_no_retweeted


def batch_split_ouput(num_file, num_xlsx):
    record_txt = f'H:\\output_split\\democratic\\{num_file}.txt'

    for i in range(0, num_xlsx + 1):  # 生成0_output.xlsx-num_output.xslx
        input_xlsx = f"H:\\democratic\\democratic-candidate-filter-ids-{num_file}-output\\democratic-candidate-filter-ids-{num_file}-ok-{i}-output.xlsx"
        output_xlsx_exist_url = f'H:\\output_split\\democratic\\{num_file}_exist_url\\{num_file}-{i}-exist_url.xlsx'
        output_xlsx_without_url = f'H:\\output_split\\democratic\\{num_file}_without_url\\{num_file}-{i}-without_url.xlsx'
        output_xlsx_no_retweeted = f'H:\\output_split\\democratic\\{num_file}_no_retweeted\\{num_file}-{i}-no-retweeted.xlsx'
        print("-----------------------------------------------------------------------------------------------------")
        print(input_xlsx)
        print(output_xlsx_exist_url)
        print(output_xlsx_without_url)
        print(output_xlsx_no_retweeted)
        print(record_txt)
        count_exist_url, count_without_url, count_no_retweeted = split_output(input_xlsx, output_xlsx_exist_url, output_xlsx_without_url, output_xlsx_no_retweeted )
        with open(record_txt, 'a', encoding='utf-8') as rt:
            print_string = f"democratic-{num_file}-{i}：exist_url: {count_exist_url}\t\twithout_url: {count_without_url}\t\tno_retweeted: {count_no_retweeted}\n"
            rt.write(print_string)


if __name__ == "__main__":
    # split_output("H:\\demo\\demo_split_output.xlsx", "H:\\demo\\result_split_output.xlsx")
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

    for i in range(3, 18):

        print("=====================================================================================================")
        output_folder = f'H:\\output_split\\democratic\\{i}_exist_url'
        # 检查文件夹是否存在
        if not os.path.exists(output_folder):
            # 如果不存在，创建文件夹
            os.makedirs(output_folder)
            print(f"Folder '{output_folder}' created.")
        else:
            print(f"Folder '{output_folder}' already exists.")

        output_folder = f'H:\\output_split\\democratic\\{i}_without_url'
        # 检查文件夹是否存在
        if not os.path.exists(output_folder):
            # 如果不存在，创建文件夹
            os.makedirs(output_folder)
            print(f"Folder '{output_folder}' created.")
        else:
            print(f"Folder '{output_folder}' already exists.")

        output_folder = f'H:\\output_split\\democratic\\{i}_no_retweeted'
        # 检查文件夹是否存在
        if not os.path.exists(output_folder):
            # 如果不存在，创建文件夹
            os.makedirs(output_folder)
            print(f"Folder '{output_folder}' created.")
        else:
            print(f"Folder '{output_folder}' already exists.")

        batch_split_ouput(i, file_num[i])

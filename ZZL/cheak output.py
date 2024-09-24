import os
import pandas as pd


def count_rows_in_csv_files(root_folder):
    folder_totals = {}
    grand_total = 0

    for subdir, _, files in os.walk(root_folder):
        if subdir == root_folder:
            continue  # 跳过根文件夹

        folder_total = 0
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(subdir, file)
                print(file_path)
                try:
                    df = pd.read_csv(file_path, dtype=str)
                    row_count = len(df)
                    folder_total += row_count
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

        folder_name = os.path.basename(subdir)
        folder_totals[folder_name] = folder_total
        grand_total += folder_total

    return folder_totals, grand_total






if __name__ == '__main__':

    root_folder = 'F:\\us-presidential-output-with-Linebreak'  # 替换为你的根文件夹路径
    folder_totals, grand_total = count_rows_in_csv_files(root_folder)

    # 打印每个子文件夹的总行数
    for folder, total in folder_totals.items():
        print(f"Folder: {folder}, Total Rows: {total}")

    # 打印所有文件夹的总行数
    print(f"Grand Total Rows: {grand_total}")
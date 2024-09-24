import os

import pandas as pd


def clean_internal_newlines(csv_input_path, csv_output_path):
    # Read the CSV file into a DataFrame
    print(f"内容开始读取!")
    df = pd.read_csv(csv_input_path, escapechar="\\", header=0, dtype=str)
    print(f"内容读取成功!")

    pd.set_option('future.no_silent_downcasting', True)
    # Replace all internal line breaks in the DataFrame with a space
    cleaned_df = df.replace(to_replace=r'\r\n|\n|\r', value=' ', regex=True)
    print(f"cvs处理完成!")

    # Write the cleaned DataFrame to a new CSV file
    cleaned_df.to_csv(csv_output_path, index=False, header=True)
    print(f"cvs存储完成!")


def batch_clean_internal_newlines(folder_path, folder_name):
    for cvs_name in os.listdir(folder_path):
        print("---------------------------------------------------------------------------------------------------")
        print(cvs_name)
        input_cvs_path_batch = os.path.join(folder_path, cvs_name)
        print(input_cvs_path_batch)
        if not os.path.exists(f"H:\\us-presidential-output\\{folder_name}"):
            os.makedirs(f"H:\\us-presidential-output\\{folder_name}")
        output_cvs_path_batch = os.path.join(f"H:\\us-presidential-output\\{folder_name}\\{cvs_name}")
        print(output_cvs_path_batch)
        clean_internal_newlines(input_cvs_path_batch, output_cvs_path_batch)


if __name__ == "__main__":
    # path = "H:\\us-presidential-output-with-Linebreak"
    # for root, dirs, files in os.walk(path):
    #     for name in dirs:
    #         folder = os.path.join(root, name)
    #         print("===================================================================================================")
    #         print(name)
    #         batch_clean_internal_newlines(folder, name)

    clean_internal_newlines("H:\\demo_data\\2021-01-24-3-output.csv", "H:\\demo_data\\1.csv")

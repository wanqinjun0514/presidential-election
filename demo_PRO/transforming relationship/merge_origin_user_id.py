import glob

import pandas as pd


def merge_origin_user_id(xlsx_path, result_path):
    merged_df = pd.DataFrame()

    xlsx_files = glob.glob(f"{xlsx_path}\\*.xlsx")

    pd.set_option('expand_frame_repr', False)

    for xlsx in xlsx_files:
        print(xlsx)
        df = pd.read_excel(xlsx, sheet_name="Sheet1", header=0, dtype=str)
        # print(df)
        merged_df = merged_df._append(df, ignore_index=True)
    # print(merged_df)
    merged_df_rename = merged_df.rename(columns={'Value': 'User_id'})
    # print(merged_df_rename)

    merged_df_rename['Count'] = merged_df_rename['Count'].astype(int)
    merged_df_grouped = merged_df_rename.groupby('User_id')['Count'].sum().reset_index()
    result_df = merged_df_grouped.sort_values(by='Count', ascending=False)
    # print(result_df)

    result_df.to_excel(result_path, index=False, header=True)


def batch_merge_origin_user_id():
    for i in range(3, 18):
        input_xlsx = f"H:\\tranforming_relationship\\democratic_count\\{i}"
        output_xlsx = f"H:\\tranforming_relationship\\gather\\democratic-{i}.xlsx"
        print("-------------------------------------------------------------------------------------------------------")
        print(input_xlsx)
        merge_origin_user_id(input_xlsx, output_xlsx)

    for j in range(3, 7):
        input_xlsx = f"H:\\tranforming_relationship\\republican_count\\{j}"
        output_xlsx = f"H:\\tranforming_relationship\\gather\\republican-{j}.xlsx"
        print("-------------------------------------------------------------------------------------------------------")
        print(input_xlsx)
        merge_origin_user_id(input_xlsx, output_xlsx)

    input_xlsx = f"H:\\tranforming_relationship\\electionday_count"
    output_xlsx = f"H:\\tranforming_relationship\\gather\\electionday.xlsx"
    print("-------------------------------------------------------------------------------------------------------")
    print(input_xlsx)
    merge_origin_user_id(input_xlsx, output_xlsx)


if __name__ == "__main__":
    # merge_origin_user_id("H:\\demo\\demo_merge_origin_user_id", "H:\\demo\\demo_merge_origin_user_id\\result.xlsx")

    batch_merge_origin_user_id()
    input_xlsx = f"H:\\tranforming_relationship\\gather"
    output_xlsx = f"H:\\tranforming_relationship\\origin_user_id_final.xlsx"
    print("-------------------------------------------------------------------------------------------------------")
    print(input_xlsx)
    merge_origin_user_id(input_xlsx, output_xlsx)

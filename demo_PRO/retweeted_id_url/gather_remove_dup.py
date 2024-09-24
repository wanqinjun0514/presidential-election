# 聚合去重之后的xlsx
import pandas as pd
import glob


def gather(xlsx_path, result_path):
    combined_df = pd.DataFrame(columns=["ID", "URL"])

    xlsx_files = glob.glob(f"{xlsx_path}\\*.xlsx")

    line_num_before = 0
    line_num_after = 0

    for xlsx in xlsx_files:
        print(xlsx)
        df = pd.read_excel(xlsx, sheet_name="Sheet1", header=0, dtype=str)
        # print(df, "\n", df.shape[0])
        combined_df = combined_df._append(df, ignore_index=True)

    # print(combined_df)
    line_num_before = combined_df.shape[0]

    combined_df_unique = combined_df.drop_duplicates(subset=['ID', 'URL'], keep='first')
    combined_df_unique.reset_index(drop=True, inplace=True)

    # print(combined_df_unique)
    line_num_after = combined_df_unique.shape[0]

    combined_df_unique.to_excel(result_path, index=False)
    return line_num_before, line_num_after


def batch_gather():
    record_txt = f'H:\\retweeted_id - url\\gather\\democratic.txt'
    for i in range(3, 18):
        input_xlsx = f"H:\\retweeted_id - url\\democratic_remove_dup\\{i}"
        output_xlsx = f"H:\\retweeted_id - url\\gather\\democratic-{i}.xlsx"
        print("-------------------------------------------------------------------------------------------------------")
        print(input_xlsx)
        line_num_before, line_num_after = gather(input_xlsx, output_xlsx)

        with open(record_txt, 'a', encoding='utf-8') as rt:
            print_string = f"democratic-{i}：line_num_before: {line_num_before}\t\tline_num_after: {line_num_after}\n"
            rt.write(print_string)

    record_txt = f'H:\\retweeted_id - url\\gather\\republican.txt'
    for j in range(3, 7):
        input_xlsx = f"H:\\retweeted_id - url\\republican_remove_dup\\{j}"
        output_xlsx = f"H:\\retweeted_id - url\\gather\\republican-{j}.xlsx"
        print("-------------------------------------------------------------------------------------------------------")
        print(input_xlsx)
        line_num_before, line_num_after = gather(input_xlsx, output_xlsx)

        with open(record_txt, 'a', encoding='utf-8') as rt:
            print_string = f"republican-{j}：line_num_before: {line_num_before}\t\tline_num_after: {line_num_after}\n"
            rt.write(print_string)

    record_txt = f'H:\\retweeted_id - url\\gather\\electionday.txt'
    input_xlsx = f"H:\\retweeted_id - url\\electionday_remove_dup"
    output_xlsx = f"H:\\retweeted_id - url\\gather\\electionday.xlsx"
    print("-------------------------------------------------------------------------------------------------------")
    print(input_xlsx)
    line_num_before, line_num_after = gather(input_xlsx, output_xlsx)

    with open(record_txt, 'a', encoding='utf-8') as rt:
        print_string = f"electionday：line_num_before: {line_num_before}\t\tline_num_after: {line_num_after}\n"
        rt.write(print_string)

if __name__ == "__main__":
    # gather("H:\\retweeted_id - url\\republican_remove_dup\\3", "H:\retweeted_id - url")
    # batch_gather()

    record_txt = f'H:\\retweeted_id - url\\id_url_final.txt'
    input_xlsx = f"H:\\retweeted_id - url\\gather"
    output_xlsx = f"H:\\retweeted_id - url\\id_url_final.xlsx"
    print("-------------------------------------------------------------------------------------------------------")
    print(input_xlsx)
    line_num_before, line_num_after = gather(input_xlsx, output_xlsx)

    with open(record_txt, 'a', encoding='utf-8') as rt:
        print_string = f"id_url_final：line_num_before: {line_num_before}\t\tline_num_after: {line_num_after}\n"
        rt.write(print_string)

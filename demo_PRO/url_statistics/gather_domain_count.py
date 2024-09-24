import glob
import pandas as pd


# import os

def gather_count(xlsx_path, result_path):
    combined_data = pd.DataFrame(columns=["Domain", "Count"])

    xlsx_files = glob.glob(f"{xlsx_path}\\*.xlsx")

    # sorted_xlsx_files = sorted(xlsx_files, key=lambda x: int(x.split("-")[1].split(".")[0]))
    # sorted_xlsx_files = sorted(xlsx_files, key=lambda x: int(x.split("\\")[-1].split(".")[0]))

    line_num = 0

    for xlsx in xlsx_files:
        print(xlsx)
        df = pd.read_excel(xlsx, sheet_name="Sheet1")
        line_num = line_num + df.shape[0]
        # print(df, "\n", df.shape[0])
        combined_data = combined_data._append(df, ignore_index=True)

    # print(combined_data, "\n", line_num)

    result = combined_data.groupby("Domain")["Count"].sum().reset_index()
    result = result.sort_values(by="Count", ascending=False)
    # print(result)
    result.to_excel(result_path, index=False)

def batch_gather_count():
    for i in range(3, 18):
        input_xlsx = f"H:\\url_statistics\\democratic\\{i}"
        output_xlsx = f"H:\\url_statistics\\gather\\democratic-{i}.xlsx"
        print("-------------------------------------------------------------------------------------------------------")
        print(input_xlsx)
        gather_count(input_xlsx, output_xlsx)

    for j in range(3, 7):
        input_xlsx = f"H:\\url_statistics\\republican\\{j}"
        output_xlsx = f"H:\\url_statistics\\gather\\republican-{j}.xlsx"
        print("-------------------------------------------------------------------------------------------------------")
        print(input_xlsx)
        gather_count(input_xlsx, output_xlsx)

    # input_xlsx = f"H:\\url_statistics\\electionday"
    # output_xlsx = f"H:\\url_statistics\\gather\\electionday.xlsx"
    # print("-------------------------------------------------------------------------------------------------------")
    # print(input_xlsx)
    # gather_count(input_xlsx, output_xlsx)


if __name__ == "__main__":
    # gather_count("H:\\url_statistics\\democratic\\3", "H:\\url_statistics\\gather\\democratic.xlsx")
    # batch_gather_count()

    gather_count("H:\\url_statistics\\gather", "H:\\url_statistics\\url_statistics_final.xlsx")

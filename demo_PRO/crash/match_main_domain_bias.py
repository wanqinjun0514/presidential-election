import pandas as pd
import re
import tldextract

# 对main_domain_count.xlsx文件添加一列bias保存在main_domain_count_with_bias.xlsx文件里
def match_main_domain_bias():
    # 读取两个文件，只读取main_domain_count.xlsx的第1列和第2列以及url_counts_marking_df的第3列和第4列
    main_domain_count_file = 'main_domain_count.xlsx'  # main_domain_count是主要域名和其出现次数
    url_counts_marking_file = 'url_counts_merged(total-marking)_main_domain.xlsx'  # url_counts_merged(total-marking)_main_domain.xlsx是一直在打分的文件 第一列是url不是主要域名

    main_domain_count_df = pd.read_excel(main_domain_count_file, usecols=[0, 1])
    url_counts_marking_df = pd.read_excel(url_counts_marking_file, usecols=[2, 3])

    # 将url_counts_marking_df的bias列添加到main_domain_count_df中作为第三列
    main_domain_count_df['bias'] = url_counts_marking_df['bias']

    # 保存结果到新的xlsx文件
    result_file_path = 'main_domain_count_with_bias.xlsx'
    main_domain_count_df.to_excel(result_file_path, index=False)

    print("匹配后的结果已保存到", result_file_path)


# 将正在打分的文件转换成只有主要域名和count的文件main_domain_count_with_bias.xlsx 与 media bias fact check网站上扒下来的表all_bias_table.xlsx进行匹配（表里都是主要域名） 保存在main_domain_count_with_updated_bias.xlsx
def match_all_bias_tables():
    # 读取main_domain_count_with_bias.xlsx和all_bias_table.xlsx
    main_domain_count_with_bias_file = 'main_domain_count_with_bias.xlsx'
    all_bias_table_file = 'all_bias_table.xlsx'

    main_domain_count_with_bias_df = pd.read_excel(main_domain_count_with_bias_file)
    all_bias_table_df = pd.read_excel(all_bias_table_file)

    # 创建一个字典来存储all_bias_table.xlsx中主要域名与bias的映射关系
    bias_mapping = dict(zip(all_bias_table_df['主要域名'], all_bias_table_df['bias']))

    # 根据主要域名匹配并更新main_domain_count_with_bias_df的第三列（bias）
    def extract_domain_from_brackets(text):
        match = re.search(r'\((.*?)\)', text)
        if match:
            return match.group(1).strip()
        return text

    def update_bias(row):
        if not pd.isna(row['bias']):
            return row['bias']

        domain = extract_domain_from_brackets(row['主要域名'])
        matched_bias = bias_mapping.get(domain, None)

        if matched_bias is not None:
            print(f"匹配成功：主要域名 '{domain}' 对应的 bias 为 {matched_bias}")

        return matched_bias

    main_domain_count_with_bias_df['bias'] = main_domain_count_with_bias_df.apply(update_bias, axis=1)

    # 保存更新后的结果到新的xlsx文件
    result_file_path = 'main_domain_count_with_updated_bias.xlsx'
    main_domain_count_with_bias_df.to_excel(result_file_path, index=False)

    print("更新后的结果已保存到", result_file_path)


# 将各个2016_url、2017_url、2018_url、2019_url、2020_url、2021_url、2022_url与main_domain_count_with_updated_bias.xlsx进行匹配 年份_url需要变成主要域名进行匹配
def year_data_match_main_domain_bias():
    # 读取main_domain_count_with_updated_bias.xlsx文件
    main_domain_count_with_updated_bias_file = 'main_domain_count_with_updated_bias.xlsx'
    main_domain_count_with_updated_bias_df = pd.read_excel(main_domain_count_with_updated_bias_file)
    file_2018 = 'F:\\OpenSource_Datasets\\2020_US_presidential_election\\page5\\vp-debate-filter-ids-separation\\merge_urls\\divided_by_time\\2022.xlsx'
    result_file_path = 'F:\\OpenSource_Datasets\\2020_US_presidential_election\\page5\\vp-debate-filter-ids-separation\\merge_urls\\divided_by_time\\2022_with_bias.xlsx'
    # 打开2018.xlsx文件
    with pd.ExcelFile(file_2018) as xls:
        # 遍历每个sheet，这里假设只有一个sheet
        for sheet_name in xls.sheet_names:
            # 读取每个sheet的内容
            file_2018_df = pd.read_excel(xls, sheet_name, header=None)

            # 定义函数来提取主要域名
            def extract_domain(row):
                url = row[2]  # 使用索引2表示第三列
                ext = tldextract.extract(url)
                main_domain = f"{ext.domain}.{ext.suffix}"
                return main_domain

            # 添加主要域名列到2018.xlsx文件
            file_2018_df['主要域名'] = file_2018_df.apply(extract_domain, axis=1)

            # 创建一个函数来匹配并添加bias
            def update_bias(row):
                domain = row['主要域名']
                matched_bias = \
                    main_domain_count_with_updated_bias_df[
                        main_domain_count_with_updated_bias_df['主要域名'] == domain][
                        'bias'].values
                return matched_bias[0] if len(matched_bias) > 0 else None

            # 添加bias列到2018.xlsx文件
            file_2018_df['bias'] = file_2018_df.apply(update_bias, axis=1)
            # 将第一列数据转换为字符串格式防止用户id被截断
            file_2018_df[0] = file_2018_df[0].astype(str)
            # 保存结果到新的xlsx文件，不保存表头
            file_2018_df.to_excel(result_file_path, index=False, header=None)

            print("匹配后的结果已保存到", result_file_path)


def match_bias():
    # 读取两个 Excel 文件
    file1 = "H:\\main_domain_count_with_updated_bias.xlsx"
    file2 = "H:\\total_new_data-maindomain_counts_merged.xlsx"

    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2, header=None)

    print("第一个 Excel 文件：")
    # print(df1.columns)
    print(df1.head())

    df2 = df2.rename(columns={0: 'domain'})  # 将第一列的列名更改为 'domain'
    df2 = df2.rename(columns={1: 'count'})  # 将第二列的列名更改为 'count'
    print("\n第二个 Excel 文件：")
    # print(df2.columns)
    print(df2.head())

    print("-----------------------------------------------------------------------------------------------------------")

    # 删除bias列为空的行
    df1.dropna(subset=['bias'], inplace=True)
    df1.to_excel('H:\\old_non-null-bias.xlsx', index=False, engine='openpyxl')
    print("完成删除bias列为空的行！！！")
    # 保留1到800行
    df2 = df2.iloc[:799]
    df2.to_excel('H:\\new_1-800.xlsx', index=False, engine='openpyxl')
    print("完成删除800以后的行！！！")

    print("-----------------------------------------------------------------------------------------------------------")

    # 提取符号"."之前的字符串作为关键字进行匹配
    df1['key'] = df1['主要域名'].apply(lambda x: x.split('.')[0])
    df2['key'] = df2['domain'].apply(lambda x: x.split('.')[0])

    print(df1.head())
    print(df2.head())

    print("----------------------------------------------------------------------------")

    # 选择bias和key列创建一个新的DataFrame
    df3 = df1[['bias', 'key']].copy()
    print(df3.head())
    df3.to_excel('H:\\old_bias_key.xlsx', index=False, engine='openpyxl')

    # 将df2中新列初始化为字符串类型
    df2['bias'] = ''
    print(df2.head())
    df2.to_excel('H:\\new_domain_count_key_bias_1-800.xlsx', index=False, engine='openpyxl')

    print("准备工作完成！")
    print("-----------------------------------------------------------------------------------------------------------")

    missing_count = 0
    for index, row in df2.iterrows():
        print(index, row['key'])
        key_temporary = row['key']
        filtered_rows = df3[df3['key'] == key_temporary]
        print(filtered_rows)
        if filtered_rows.empty:
            missing_count += 1
        else:
            # 提取filtered_rows中的bias列的值并赋给filtered_rows_bias
            filtered_rows_bias = filtered_rows['bias'].values.astype(str).tolist()
            if filtered_rows_bias:  # 检查列表是否为空
                filtered_rows_bias = filtered_rows_bias[0]  # 取第一个元素作为字符串
            else:
                filtered_rows_bias = ""  # 如果列表为空，设置为空字符串

            # 将filtered_rows_bias赋值给df2的相应行的bias列
            df2.at[index, 'bias'] = filtered_rows_bias
        print("----------------------------------------")
    print(missing_count)

    print(df2.head())
    df2.to_excel('H:\\new.xlsx', index=False, engine='openpyxl')  # 写入 Excel 文件，不包含行索引
def extract_empty_bias():

    file = "H:\\new.xlsx"
    df = pd.read_excel(file)
    print(df)

    # 选择 'bias' 列为空的行，创建一个新的 DataFrame
    missing_bias_df = df[df['bias'].isnull()]
    missing_bias_df.reset_index(drop=True, inplace=True)
    print(missing_bias_df)

    missing_bias_df.to_excel('H:\\new_missing_bias.xlsx', index=False, engine='openpyxl')


if __name__ == "__main__":
    # match_main_domain_bias()
    # match_all_bias_tables()
    # year_data_match_main_domain_bias()
    # match_bias()
    extract_empty_bias()

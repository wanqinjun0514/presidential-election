# 统计主体域名的全部拓展形式
from urllib.parse import urlparse

import pandas as pd


def simplify_url2():
    # 读取XLSX文件
    df = pd.read_excel(f'H:\\domain_extension\\total_accumulated_domain_counts_only_media.xlsx', header=None)
    print("读取完成！")
    print(df)
    df.columns = ['Domain', 'Count']
    # 初始化一个字典来存储累加的计数
    count_dict = {}
    # 初始化一个dataframe存储url
    domain_df = pd.DataFrame(columns=['Domain', 'URL'])

    i = 0
    # 遍历DataFrame
    for index, row in df.iterrows():
        # print("-------------------------------------------------------------------------------------------------------")
        print("line:", i)
        i = i + 1
        url = 'https://' + row['Domain']  # 在URL前加上https://保证格式正确
        # print("Domain:", row['Domain'])
        # print("url:", url)
        try:
            count = int(row['Count'])
        except ValueError:
            print(f"Error converting count to int for URL {url}: {row['Count']}")
            continue
        # print("Count:", count)

        # 解析URL以获取主机名
        parsed_url = urlparse(url)
        # print("parsed_url:", parsed_url)
        hostname = parsed_url.netloc
        # print("hostname:", hostname)

        # 提取主机名中的基本域名
        parts = hostname.split('.')
        # print("parts", parts)
        if len(parts) > 2 and (parts[-2] in ['co', 'com', 'net', 'org'] or parts[-1] in ['uk', 'au']):
            domain = parts[-3]  # 对.co.uk等特殊情况的处理
        else:
            domain = parts[-2]

        # print("domain:", domain)
        if domain in domain_df['Domain'].values:
            existing_index = domain_df[domain_df['Domain'] == domain].index[0]
            domain_df.at[existing_index, 'URL'] += f", {row['Domain']}"
        else:
            domain_df = domain_df._append({'Domain': domain, 'URL': row['Domain']}, ignore_index=True)

        # 累加计数
        if domain in count_dict:
            count_dict[domain] += count
        else:
            count_dict[domain] = count
    # print(domain_df)
    # print(count_dict)

    # 将字典转换为DataFrame
    result_df = pd.DataFrame(list(count_dict.items()), columns=['URL', 'Count'])

    # 将结果写入新的XLSX文件
    result_df.to_excel("H:\\domain_extension\\count_dict_wqj.xlsx", header=True, index=False)

    domain_df.to_excel("H:\\domain_extension\\domain_extension_wqj.xlsx", header=True, index=False)


def split_diff_extension():
    df = pd.read_excel(f'H:\\domain_extension\\domain_extension_zzl.xlsx', header=0)

    print(df)

    df_domain_url = pd.DataFrame(columns=['Domain', 'URL'])
    i = 0

    for index, row in df.iterrows():
        # print("-------------------------------------------------------------------------------------------------------")
        print("line:", i)
        all_url = row['URL']
        # print(all_url)
        prats_one_url = all_url.split(',')
        for one_url in prats_one_url:
            # print(one_url)
            df_domain_url = df_domain_url._append({'Domain': row['Domain'], 'URL': one_url}, ignore_index=True)

    print(df_domain_url)

    # 去除第二列URL前面的空格
    df_domain_url['URL'] = df_domain_url['URL'].str.strip()

    df_domain_url.to_excel("H:\\domain_extension\\spilt_diff_extension_zzl.xlsx", index=False)


if __name__ == "__main__":
    # split_diff_extension()

    # 读取第一个文件
    df1 = pd.read_excel("H:\\domain_extension\\spilt_diff_extension_zzl.xlsx", header=0)
    # 读取第二个文件
    df2 = pd.read_excel("H:\\domain_extension\\spilt_diff_extension_wqj.xlsx", header=0)

    print(df1.head(100))
    print(df2.head(100))

    # 合并两个DataFrame
    combined_df = pd.concat([df1, df2])
    print(combined_df.head(100))

    # 去除重复行，只保留第一次出现的行
    deduplicated_df = df1.drop_duplicates(subset=['Domain', 'URL'])
    print(deduplicated_df.head(100))

    # 重新索引DataFrame
    deduplicated_df = deduplicated_df.reset_index(drop=True)
    print(deduplicated_df.head(100))

    # 保存结果到新文件
    deduplicated_df.to_excel("H:\\domain_extension\\spilt_diff_extension_merged.xlsx", index=False, header=True)

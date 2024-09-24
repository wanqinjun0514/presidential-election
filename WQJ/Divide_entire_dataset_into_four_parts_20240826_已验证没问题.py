import pandas as pd
import os
import ast
#根据retweet_expanded_urls_array字段把一个csv文件拆分成三个csv，文件名不改变
# 但是放入当前目录下的三个文件夹里：名为without_url的文件夹、external_url、twitter_url。
# 具体拆分流程是：读取每一行的retweet_expanded_urls_array字段，
# 如果该字段为空，则把这行数据放在without_url文件夹下同名文件里，
# 如果字段为https://twitter.com/开头的话就这行数据放在twitter_url文件夹下同名文件里，
# 其他情况放入external_url里。而且注意：读取所有字段请以str形式来读取
month = '2019_13'


# 创建目录（如果不存在）
os.makedirs(rf'F:\three_parts_output\without_url\output_{month}', exist_ok=True)
os.makedirs(rf'F:\three_parts_output\single_url\twitter_url\output_{month}', exist_ok=True)
os.makedirs(rf'F:\three_parts_output\single_url\external_url\output_{month}', exist_ok=True)
os.makedirs(rf'F:\three_parts_output\multiple_urls\output_{month}', exist_ok=True)
os.makedirs(rf'F:\three_parts_output\retweet_and_quote\output_{month}', exist_ok=True)

# 读取CSV文件
# 定义文件夹路径
input_folder = rf'F:\us-presidential-output\output_{month}'

# 获取文件夹下所有CSV文件的文件名
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]  # 将此路径替换为实际的CSV文件路径

# 初始化总行数
total_row_count = 0

# 初始化四个数组用于存储分类后的行数
without_url_count = 0
external_url_count = 0
twitter_url_count = 0
multiple_urls_count = 0
retweet_and_quote_urls_count = 0

# 定义分类和保存行的函数
def classify_rows(row):
    global without_url_count, external_url_count, twitter_url_count, multiple_urls_count, retweet_and_quote_urls_count
    retweet_urls = row.get('retweet_expanded_urls_array', None)
    quoted_urls = row.get('quoted_expanded_urls_array', None)

    if pd.isna(retweet_urls) or retweet_urls == '':
        retweet_urls = None
    if pd.isna(quoted_urls) or quoted_urls == '':
        quoted_urls = None
    # 如果两个字段都为空
    if retweet_urls is None and quoted_urls is None:
        without_url_rows.append(row)
        without_url_count += 1
    elif retweet_urls is not None and quoted_urls is not None:
        # 如果两个字段都不为空
        retweet_and_quote_rows.append(row)
        retweet_and_quote_urls_count += 1
    else:
        # 处理只有一个字段不为空的情况
        url_field = retweet_urls if retweet_urls is not None else quoted_urls
        url_field = url_field.strip('"')  # 去掉字段前后的引号
        urls = url_field.split(',')  # 使用逗号分隔URL

        if len(urls) == 1:
            url = urls[0].strip()
            if url.startswith('https://twitter.com/'):
                twitter_url_rows.append(row)
                twitter_url_count += 1
            else:
                external_url_rows.append(row)
                external_url_count += 1
        else:
            multiple_urls_rows.append(row)
            multiple_urls_count += 1


def save_to_csv(rows, folder, file_name):
    if rows:
        output_path = os.path.join(folder, file_name)
        pd.DataFrame(rows).to_csv(output_path, index=False)


# 遍历所有CSV文件
for csv_file in csv_files:
    file_path = os.path.join(input_folder, csv_file)
    # 读取CSV文件
    df = pd.read_csv(file_path, dtype=str)
    total_row_count += len(df)
    print('----------------------------------------------------------')
    print('正在处理文件：', file_path)

    # 初始化五个数组用于存储分类后的行
    without_url_rows = []
    external_url_rows = []
    twitter_url_rows = []
    multiple_urls_rows = []
    retweet_and_quote_rows = []

    # 对每一行进行分类并存储到相应的数组中
    for index, row in df.iterrows():
        classify_rows(row)
        if index % 1000 == 0:
            print(f"Processed row {index} in file {csv_file}")

    # 将分类后的数据保存到对应的CSV文件中
    save_to_csv(without_url_rows, rf'F:\three_parts_output\without_url\output_{month}', os.path.basename(file_path))
    save_to_csv(external_url_rows, rf'F:\three_parts_output\single_url\external_url\output_{month}',
                os.path.basename(file_path))
    save_to_csv(twitter_url_rows, rf'F:\three_parts_output\single_url\twitter_url\output_{month}',
                os.path.basename(file_path))
    save_to_csv(multiple_urls_rows, rf'F:\three_parts_output\multiple_urls\output_{month}', os.path.basename(file_path))
    save_to_csv(retweet_and_quote_rows, rf'F:\three_parts_output\retweet_and_quote\output_{month}',
                os.path.basename(file_path))

# 数据量检查
print(f"总数据量: {total_row_count}")
print(f"没有URL的数据量: {without_url_count}")
print(f"外部URL的数据量: {external_url_count}")
print(f"Twitter URL的数据量: {twitter_url_count}")
print(f"多URL的数据量: {multiple_urls_count}")
print(f"Retweet和Quote都有的数据量: {retweet_and_quote_urls_count}")

total_split_count = without_url_count + external_url_count + twitter_url_count + multiple_urls_count + retweet_and_quote_urls_count
print("\n数据量检查：",without_url_count,"+",external_url_count,"+",twitter_url_count,"+",multiple_urls_count,"+",retweet_and_quote_urls_count,"=",total_split_count)

if total_split_count == total_row_count:
    print("数据量检查通过：拆分后的数据量之和等于总数据量。")
else:
    print(f"数据量检查失败：拆分后的数据量之和 ({total_split_count}) 不等于总数据量 ({total_row_count})。")

print("所有CSV文件已成功拆分并保存到相应的文件夹中。")
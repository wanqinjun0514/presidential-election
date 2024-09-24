import pandas as pd



def wash_data():

    # 设置显示选项，取消列宽限制
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    # 读取 CSV 文件
    file_path = 'F:\\fianl data\\media bias\\media-bias-final-username.csv'  # 将此处替换为你的文件路径
    df = pd.read_csv(file_path, dtype=str, header=None)

    # 检查第四列有几种值，并统计每种值的出现次数
    value_counts = df.iloc[:, 3].value_counts()  # 第四列的索引是3

    # 输出统计结果
    print(f"第四列有 {value_counts.shape[0]} 种不同的值。")
    print(value_counts)

    # 检测第三列是否有重复值
    duplicates = df.iloc[:, 2].duplicated()

    # 如果存在重复值，输出对应的行
    if duplicates.any():
        print("第三列存在重复值，重复的行如下：")
        print(df[duplicates])
    else:
        print("第三列没有重复值。")

if __name__ == "__main__":
    wash_data()



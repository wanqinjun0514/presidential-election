import pandas as pd


def cheak_url_num():
    import pandas as pd

    # 读取CSV文件
    df1 = pd.read_csv('F:\\fianl data\\media bias\\media-bias-final-username.csv', dtype=str, header=0, index_col=None, encoding='utf-8')
    df2 = pd.read_csv('F:\\fianl data\\twitter-username.csv', dtype={"username": str, "counts": int}, header=0, index_col=None, encoding='utf-8')

    print(df1)
    print(df2)

    # 提取第一个CSV中url的域名
    df1['username'] = df1['Username'].apply(lambda x: x.split('/')[2] if '//' in x else x.split('/')[0])

    # 合并两个DataFrame，使用Domain作为键
    merged_df = pd.merge(df1, df2, how='left', left_on='username', right_on='username')

    print(merged_df)

    # 计算count的总和
    total_count_sum = merged_df['counts'].sum()

    # 输出结果
    print("Total Count Sum:", total_count_sum)

    # # 保存结果到新的CSV文件
    # df_media.to_csv('output_csv.csv', index=False)
    #
    # print("操作完成，结果已保存到 output_csv.csv")















if __name__ == "__main__":

    # 设置显示选项，取消列宽限制
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    cheak_url_num()



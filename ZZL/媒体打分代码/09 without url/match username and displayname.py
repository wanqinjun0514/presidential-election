import pandas as pd


def match_username_and_displayname():
    # 读取两个 CSV 文件
    df1 = pd.read_csv('F:\\fianl data\\media bias\\media-bias-final-username.csv')
    df2 = pd.read_csv('F:\\fianl data\\username and displayname.csv')

    not_num = 0

    # 创建两个新的列，分别存放displayname和id_str
    df1['displayname'] = ''
    df1['id_str'] = ''

    # 将所有username转换为小写
    df1['Username_lower'] = df1['Username'].str.lower()
    df2['username_lower'] = df2['username'].str.lower()

    # 遍历第一个CSV文件的每一行
    for index, row in df1.iterrows():
        username = row['Username_lower']

        # 在第二个CSV文件中查找是否存在相同的username（不区分大小写）
        matching_row = df2[df2['username_lower'] == username]

        if not matching_row.empty:
            # 如果存在匹配项，添加displayname和id_str到对应行
            df1.at[index, 'displayname'] = matching_row.iloc[0]['displayname']
            df1.at[index, 'id_str'] = matching_row.iloc[0]['id_str']
        else:
            # 如果不存在，打印对应的Username
            print(f"Username not found: {row['Username']}")
            not_num += 1

    # 删除临时列
    df1.drop(columns=['Username_lower'], inplace=True)
    df2.drop(columns=['username_lower'], inplace=True)

    print(not_num)

    # 保存更新后的第一个CSV文件
    df1.to_csv('F:\\fianl data\\media bias\\media-bias-final-username-display1.csv', index=False)


if __name__ == "__main__":
    match_username_and_displayname()

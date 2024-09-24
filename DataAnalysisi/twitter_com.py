import os
import pandas as pd



def statistics_user_name_id():
    # 主文件夹路径
    main_folder = 'H:\\with_url_data\\with_twitter'

    # 创建一个空的DataFrame来存储统计结果
    username_counts = pd.DataFrame(columns=['username', 'counts'])

    # 遍历主文件夹中的每个子文件夹
    for subfolder in os.listdir(main_folder):
        subfolder_path = os.path.join(main_folder, subfolder)

        if os.path.isdir(subfolder_path):
            # 遍历子文件夹中的每个文件
            for file in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, file)
                print(file_path)

                if file.endswith('.csv'):
                    # 读取CSV文件
                    data = pd.read_csv(file_path, header=0, dtype=str)

                    # 统计每个唯一的username出现的次数
                    counts = data['username'].value_counts().reset_index()
                    counts.columns = ['username', 'counts']

                    # 将当前的统计结果与累积的统计结果合并
                    username_counts = username_counts.merge(
                        counts,
                        on='username',
                        how='outer',
                        suffixes=('', '_new')
                    ).fillna(0)

                    # 使用infer_objects处理可能的类型推断问题
                    username_counts = username_counts.infer_objects(copy=False)

                    # 更新counts列的值
                    username_counts['counts'] = username_counts['counts'] + username_counts['counts_new']
                    username_counts = username_counts.drop(columns=['counts_new'])

    # 对统计结果按出现次数降序排序
    username_counts = username_counts.sort_values(by='counts', ascending=False)

    # 打印统计结果
    print(username_counts)

    # 保存排序后的统计结果
    username_counts.to_csv('H:\\with_url_data\\twitter-username.csv', index=False)

def data():
    data = pd.read_csv('H:\\with_url_data\\twitter-username.csv', header=0)
    print(data)

    # 计算counts列的总和
    total_counts = data['counts'].sum()

    # 计算前三百个username的counts总和
    top_300_counts = data.head(300)['counts'].sum()
    top_500_counts = data.head(500)['counts'].sum()
    top_1000_counts = data.head(1000)['counts'].sum()
    top_2000_counts = data.head(2000)['counts'].sum()
    top_3000_counts = data.head(3000)['counts'].sum()
    top_10000_counts = data.head(10000)['counts'].sum()

    print(f"twitter出现次数:{total_counts}")
    print(f"twitter前300出现次数:{top_300_counts}    占比：{top_300_counts / total_counts}")
    print(f"twitter前500出现次数:{top_500_counts}    占比：{top_500_counts / total_counts}")
    print(f"twitter前1000现次数:{top_1000_counts}    占比：{top_1000_counts / total_counts}")
    print(f"twitter前2000出现次数:{top_2000_counts}    占比：{top_2000_counts / total_counts}")
    print(f"twitter前3000出现次数:{top_3000_counts}    占比：{top_3000_counts / total_counts}")
    print(f"twitter前10000出现次数:{top_10000_counts}    占比：{top_10000_counts / total_counts}")


if __name__ == "__main__":
    # statistics_user_name_id()
    data()


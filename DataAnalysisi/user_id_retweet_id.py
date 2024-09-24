import os
import pandas as pd
import glob

def id_count(folder_path, result_path, record_path):
    # 字典来存储每个retweeted_user_id对应的所有retweeted_id
    retweeted_map = {}
    df_data = []


    # 遍历文件夹中的每个文件
    for filename in os.listdir(folder_path):

        retweeted_id_num = 0
        retweeted_user_id_num = 0

        # 确保处理的是CSV文件
        print(filename)
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            # print(file_path)
            # 读取第二列(retweeted_id)和第三列(retweeted_user_id)
            data = pd.read_csv(file_path, usecols=[1, 2], header=0, dtype=str)
            # print(data)

            # 更新字典
            for _, row in data.iterrows():
                retweeted_id = row.iloc[0]
                retweeted_user_id = row.iloc[1]
                if retweeted_user_id not in retweeted_map:
                    retweeted_user_id_num += 1
                    retweeted_map[retweeted_user_id] = set()
                retweeted_id_num += 1
                retweeted_map[retweeted_user_id].add(retweeted_id)

            with open(record_path, 'a', encoding='utf-8') as rt:
                print_string = f"{filename}: retweeted_id_num:{retweeted_id_num}\t\tretweeted_user_id_num{retweeted_user_id_num}\n"
                rt.write(print_string)

    # # 打印每个retweeted_user_id及其所有的retweeted_id
    # for user_id, ids in retweeted_map.items():
    #     print(f"User ID {user_id} has retweeted IDs: {ids}")

    # 遍历字典，并创建适合DataFrame的数据结构
    for user_id, ids in retweeted_map.items():
        # 将ids集合转换为逗号分隔的字符串
        ids_str = ','.join(str(id) for id in ids)
        # 将每个条目作为一个列表添加到data中
        df_data.append([user_id, ids_str])

    # 将数据转换为DataFrame
    df = pd.DataFrame(df_data, columns=['retweeted_user_id', 'retweeted_ids'])

    # 将DataFrame保存到CSV文件中
    df.to_csv(result_path, index=False)


def batch_id_count(folder_path, folder_name):
    for cvs_name in os.listdir(folder_path):
        print("---------------------------------------------------------------------------------------------------")
        print(cvs_name)
        cvs_path_batch = os.path.join(folder_path, cvs_name)
        print(cvs_path_batch)



def cheak_():

    df = pd.read_csv("H:\\demo_data\\id\\2019-12-01-2-output.csv", dtype=str, header=0)

    # 设置显示选项
    pd.set_option('display.max_columns', None)  # 不限制列数
    pd.set_option('display.width', None)  # 根据内容自动调整输出宽度

    print(df)

    unique_count = df['retweeted_user_id'].nunique()

    print(f"Number of unique values in 'column_name': {unique_count}")

def merge():
    # 指定包含多个 CSV 文件的文件夹路径
    path = 'H:\\user_id_retweet_id\\id-map'
    all_files = glob.glob(path + "/*.csv")

    # 创建一个空的 DataFrame 用于存储合并后的数据
    merged_data = pd.DataFrame()

    # 读取每一个文件并合并
    for filename in all_files:
        print(filename)
        df = pd.read_csv(filename, header=0, dtype=str)
        # 合并到总数据框
        merged_data = pd.concat([merged_data, df])

    # 通过 groupby 和 join 将相同的 retweeted_user_id 的 retweeted_ids 合并
    final_data = merged_data.groupby('retweeted_user_id')['retweeted_ids'].apply(lambda x: ','.join(x)).reset_index()

    # 保存到新的 CSV 文件
    final_data.to_csv('H:\\user_id_retweet_id\\user_id_retweet_id.csv', index=False)

def cheak_final():
    df = pd.read_csv('H:\\user_id_retweet_id\\user_id_retweet_id.csv', dtype=str, header=0)

    # 设置显示选项
    pd.set_option('display.max_columns', None)  # 不限制列数
    pd.set_option('display.width', None)  # 根据内容自动调整输出宽度
    # pd.set_option('display.max_colwidth', None)
    print(df)

    # 逐行打印retweeted_ids列的值
    for index, row in df.iterrows():
        if index < 10:  # 只打印前十行
            print(f"{row['retweeted_user_id']}: {row['retweeted_ids']}")



if __name__ == "__main__":
    # path = "H:\\us-presidential-output"
    # for root, dirs, files in os.walk(path):
    #     for name in dirs:
    #         folder = os.path.join(root, name)
    #         print("===================================================================================================")
    #         print(name)
    #         print(folder)
    #         print(f"H:\\user_id_retweet_id\\id-map\\{name}_id_map.csv")
    #         print(f"H:\\user_id_retweet_id\\record\\{name}.txt")
            # id_count(folder, f"H:\\user_id_retweet_id\\id-map\\{name}_id_map.csv", f"H:\\user_id_retweet_id\\record\\{name}.txt")

    # id_count("H:\\demo_data\\id", "H:\\demo_data\\id\\id.csv", "H:\\demo_data\\id\\recoed.txt")

    # name = "output_2021_01"
    # print("===================================================================================================")
    # print(name)
    # print(f"H:\\us-presidential-output\\{name}")
    # print(f"H:\\user_id_retweet_id\\id-map\\{name}_id_map.csv")
    # print(f"H:\\user_id_retweet_id\\record\\{name}.txt")
    # id_count(f"H:\\us-presidential-output\\{name}", f"H:\\user_id_retweet_id\\id-map\\{name}_id_map.csv",f"H:\\user_id_retweet_id\\record\\{name}.txt")
    #
    # name = "output_2021_02"
    # print("===================================================================================================")
    # print(name)
    # print(f"H:\\us-presidential-output\\{name}")
    # print(f"H:\\user_id_retweet_id\\id-map\\{name}_id_map.csv")
    # print(f"H:\\user_id_retweet_id\\record\\{name}.txt")
    # id_count(f"H:\\us-presidential-output\\{name}", f"H:\\user_id_retweet_id\\id-map\\{name}_id_map.csv",
    #          f"H:\\user_id_retweet_id\\record\\{name}.txt")

    # merge()
    cheak_final()



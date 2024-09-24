import pandas as pd
import glob
import os

def single_political_influenced_user_set():
    # 定义源目录和目标文件路径
    source_directory = r"G:\us-presidential-output"
    output_directory = r"G:\set_of_users_influenced_by_top_100_politicians"
    political_user_id = '939091'# G:\record\count_user_id_record\origin_retweet_user\matched_origin_retweet_user_names_with_count_with_bias_top100.csv

    output_file = os.path.join(output_directory, f"{political_user_id}-influenced_users_set.csv")
    # 查找所有符合条件的文件
    csv_files = glob.glob(os.path.join(source_directory, "**/*-output.csv"), recursive=True)
    # 初始化一个空的集合来保存所有受影响的用户ID
    influenced_users_set = set()
    # 遍历每个文件
    for file_path in csv_files:
        df = pd.read_csv(file_path, dtype={'retweet_origin_user_id': str, 'retweeted_user_id': str})
        print('正在处理文件：', file_path)
        # 筛选受到25073877用户影响的行
        influenced_rows = df[df['retweet_origin_user_id'] == political_user_id]
        # 将受影响的retweeted_user_id添加到集合中
        influenced_users_set.update(influenced_rows['retweeted_user_id'])
    # 将集合转换为DataFrame然后保存到CSV，不包含索引和表头
    pd.DataFrame(list(influenced_users_set)).to_csv(output_file, index=False, header=False)



def multi_political_influenced_user_set():
    # 定义源目录和目标文件路径
    source_directory = r"H:\us-presidential-output"
    output_directory = r"H:\set_of_users_influenced_by_top_100_politicians"

    # 政治用户ID列表，示例中仅包含两个ID，根据需要添加更多
    political_user_ids = ['21001599', '967027984426242053', '970207298', '91882544', '78523300', '11134252', '216065430', '942156122', '15976705', '19211550', '15115280', '16581604', '813286', '166751745', '4091551984', '778763106289758208', '288277167', '786309892990574592', '101816065', '38495835', '148529707', '1917731', '818927131883356161', '21522338', '2421067430', '3530404094', '49698134', '25202268', '39349894', '14529929', '22203756', '878247600096509952', '138203134', '620571475', '225265639', '1339835893', '2800581040', '1651522832', '2836421', '26487169', '26637348', '15220768', '19568591', '455684839', '240454812', '818948638890217473', '27995424', '22677397', '759251', '601535938', '41634520', '1003107003693137921', '18247062', '798973032362606600', '548384458', '713839291210792960', '18382184', '43014978', '739610364975808513']
                           # 示例ID

    # 查找所有符合条件的文件
    csv_files = glob.glob(os.path.join(source_directory, "**/*-output.csv"), recursive=True)

    # 遍历每个政治用户ID
    for political_user_id in political_user_ids:
        influenced_users_set = set()  # 为每个政治用户初始化一个空的集合
        output_file = os.path.join(output_directory, f"{political_user_id}-influenced_users_set.csv")

        # 遍历每个文件
        for file_path in csv_files:
            df = pd.read_csv(file_path, dtype={'retweet_origin_user_id': str, 'retweeted_user_id': str},usecols=['retweet_origin_user_id', 'retweeted_user_id'])
            print(f'正在处理文件：{file_path}，寻找受{political_user_id}影响的用户')

            # 筛选受当前政治用户影响的行
            influenced_rows = df[df['retweet_origin_user_id'] == political_user_id]

            # 将受影响的retweeted_user_id添加到集合中
            influenced_users_set.update(influenced_rows['retweeted_user_id'])

        # 将集合转换为DataFrame然后保存到CSV，不包含索引和表头
        pd.DataFrame(list(influenced_users_set)).to_csv(output_file, index=False, header=False)
        print(f'已生成{political_user_id}-influenced_users_set.csv')




if __name__ == "__main__":
    # single_political_influenced_user_set()
    multi_political_influenced_user_set()
import os
from urllib.parse import urlparse
import pandas as pd
import logging



def build_username_score_dict(file_path):
    # 读取媒体url标签文件的Url和bias列
    df = pd.read_csv(file_path, header=0, dtype=str, index_col=False)

    # 定义转换规则
    bias_mapping = {
        'Extreme Bias Right': 3,
        'Right': 2,
        'Right Leaning': 1,
        'Center': 0,
        'Left Leaning': -1,
        'Left': -2,
        'Extreme Bias Left': -3,
        'Fake News': 3,
    }
    # # 调试：打印df内容
    print(df)
    # 统计每个类别的bias在csv中有多少条数据
    bias_counts = df['bias'].value_counts()

    # 输出统计结果
    print("Bias Category Counts in CSV:")
    for bias, count in bias_counts.items():
        print(f"{bias}: {count} entries")
    # 构建url-score字典，将bias转换为分数，并使用Url作为键
    df['score'] = df['bias'].map(bias_mapping).fillna(0).astype(int)

    print(df)

    # 将Url和score列转换为字典
    url_score = dict(zip(df['id_str'].str.strip(), df['score']))
    # 统计url_score字典里每类bias的数量
    score_counts = pd.Series(url_score.values()).value_counts()

    # 输出统计结果
    print("Bias Category Counts in url_score Dictionary:")
    for score, count in score_counts.items():
        bias_category = [k for k, v in bias_mapping.items() if v == score]
        if bias_category:
            print(f"{bias_category[0]} (score {score}): {count} entries")
        else:
            print(f"Unmapped score {score}: {count} entries")
    return url_score






def user_bias_by_without_url():

    # 构建url-score字典
    url_score_file_path = f"F:\\fianl data\\media bias\\media-bias-final-username-display.csv"
    url_score = build_username_score_dict(url_score_file_path)
    print(url_score)

    # '2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
    months = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
              '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02', ]
    # months = ['2019_12']

    for month in months:
        print(
            f"{month}=========================================================================================================")
        every_mouth_retweet_num = 0
        every_mouth_quoted_num = 0
        every_mouth_not_num = 0
        every_mouth_other_num = 0
        every_mouth_retweet_have_soure_num = 0
        every_mouth_quoted_have_num = 0
        # 创建两个字典来保存用户id和相应的分数及次数    `
        user_bias_score = {}
        user_appearance_count = {}
        # 文件夹路径
        folder_path = f"I:\\four\\three_parts_output\\without_url\\output_{month}"
        # folder_path = f"I:\\four\\three_parts_output\\test\\output_{month}"
        # 遍历文件夹下所有以-output.csv结尾的文件
        for filename in os.listdir(folder_path):
            if filename.endswith("-output.csv"):
                # print(folder_path)
                # print(filename)
                file_path = os.path.join(folder_path, filename)
                # print(file_path)
                df = pd.read_csv(file_path, usecols=['retweeted_user_id', 'retweet_origin_user_id',
                                                     'quoted_origin_user_id'],
                                 dtype={'retweeted_user_id': 'str', 'retweet_origin_user_id': 'str',
                                        'quoted_origin_user_id': 'str'})
                # print(df)
                print('正在处理：', file_path)

                for index, row in df.iterrows():
                    user_id = row['retweeted_user_id']
                    retweet_user_id = row['retweet_origin_user_id']  # 分隔多个URL
                    quoted_user_id = row['quoted_origin_user_id']  # 分隔多个URL

                    if pd.notna(retweet_user_id):
                        # print(f"{user_id}   1")
                        every_mouth_retweet_num += 1
                        score = url_score.get(retweet_user_id)  # 使用get方法获取分数，若不存在则返回None

                        if score is not None:  # 仅当domain存在于url_score时继续执行
                            every_mouth_retweet_have_soure_num += 1
                            if user_id in user_bias_score:
                                user_bias_score[user_id] += score
                                user_appearance_count[user_id] += 1
                            else:
                                user_bias_score[user_id] = score
                                user_appearance_count[user_id] = 1
                    elif pd.notna(quoted_user_id):
                        # print(f"{user_id}   2")
                        every_mouth_quoted_num += 1
                        score = url_score.get(quoted_user_id)  # 使用get方法获取分数，若不存在则返回None

                        if score is not None:  # 仅当domain存在于url_score时继续执行
                            every_mouth_quoted_have_num += 1
                            if user_id in user_bias_score:
                                user_bias_score[user_id] += score
                                user_appearance_count[user_id] += 1
                            else:
                                user_bias_score[user_id] = score
                                user_appearance_count[user_id] = 1
                    elif pd.isna(retweet_user_id) and pd.isna(quoted_user_id):
                        # print(f"{user_id}   3")
                        every_mouth_not_num += 1
                    else:
                        every_mouth_other_num += 1

        print(
            f"retweet_num:{every_mouth_retweet_num}\tquoted_num:{every_mouth_quoted_num}\tnot_num:{every_mouth_not_num}\tother_num:{every_mouth_other_num}\t"
            f"retweet_have_soure_num:{every_mouth_retweet_have_soure_num}\tquoted_have_num:{every_mouth_quoted_have_num}")

        # 配置日志
        logging.basicConfig(filename='without bias.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # 格式化字符串
        log_message = (
            f"retweet_num:{every_mouth_retweet_num}\tquoted_num:{every_mouth_quoted_num}\tnot_num:{every_mouth_not_num}\tother_num:{every_mouth_other_num}\t"
            f"retweet_have_soure_num:{every_mouth_retweet_have_soure_num}\tquoted_have_num:{every_mouth_quoted_have_num}")

        # 记录日志
        logging.info(log_message)

        # 将两个字典合并到一个DataFrame中
        user_stats = pd.DataFrame({
            'user_id': list(user_bias_score.keys()),
            'total_score': list(user_bias_score.values()),
            'appearance_count': list(user_appearance_count.values())
        })

        print(user_stats)

        # 保存为CSV文件
        output_path = f"I:\\four\\Experimental Results\\Average_Bias_Rating\\media_average_rating\\without_url-rating\\user_bias_scores_{month}.csv"

        user_stats.to_csv(output_path, index=False)









if __name__ == "__main__":
    # 设置显示选项，取消列宽限制
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    user_bias_by_without_url()











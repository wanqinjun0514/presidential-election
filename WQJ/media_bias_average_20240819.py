import os
import pandas as pd
from urllib.parse import urlparse


def extract_domain(url):
    try:
        return urlparse(url).netloc
    except Exception as e:
        return None


def clean_bias_labels(df, column_name='bias'):
    # 将bias列转换为小写并去除前后空格
    df[column_name] = df[column_name].str.lower().str.strip()

    # 定义映射规则，将相似或常见的错误标签映射为标准标签
    cleaning_mapping = {
        'extreme bias right': 'extreme bias right',
        'right': 'right',
        'right leaning': 'right leaning',
        'center': 'center',
        'left leaning ': 'left leaning', # 去除右侧多余的空格
        ' left leaning ': 'left leaning',  # 去除右侧多余的空格
        ' left leaning': 'left leaning',  # 去除右侧多余的空格
        'left': 'left',
        'extreme bias left': 'extreme bias left',
        'fake news': 'fake news',  # 若fake news属于不想要的类别，可考虑移除或归类
        'right ': 'right',  # 去除右侧多余的空格
        'left leaning': 'left leaning',
        'extreme bias right': 'extreme bias right',
        'extreme bias left': 'extreme bias left',
        'right leaning': 'right leaning'
    }

    # 仅保留在mapping中的类别
    df[column_name] = df[column_name].map(cleaning_mapping).fillna('other')

    return df[df[column_name] != 'other']


def build_url_score_dict(file_path):
    # 读取媒体url标签文件的domain和bias列
    df = pd.read_csv(file_path, usecols=['domain', 'bias'], dtype={'domain': 'str', 'bias': 'str'})

    # 定义转换规则
    bias_mapping = {
        'extreme bias right': 3,
        'right': 2,
        'right leaning': 1,
        'center': 0,
        'left leaning': -1,
        'left': -2,
        'extreme bias left': -3,
        'fake news': 3,
    }
    # # 调试：打印df内容
    # print(df)
    # 统计每个类别的bias在csv中有多少条数据
    bias_counts = df['bias'].value_counts()

    # 输出统计结果
    print("Bias Category Counts in CSV:")
    for bias, count in bias_counts.items():
        print(f"{bias}: {count} entries")
    # 构建url-score字典，将bias转换为分数，并使用domain作为键
    df['score'] = df['bias'].map(bias_mapping).fillna(0).astype(int)

    # 将domain和score列转换为字典
    url_score = dict(zip(df['domain'].str.strip(), df['score']))
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





def user_bias_by_media():

    # 构建url-score字典
    url_score_file_path = r"F:\Experimental Results\media-bias-final-url-cleaned.csv"
    url_score = build_url_score_dict(url_score_file_path)
    print(url_score)

    # 用于累计所有月份的用户分数和出现次数
    overall_user_bias_score = {}
    overall_user_appearance_count = {}
    months = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08', '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02',]
    for month in months:
        # 创建两个字典来保存用户id和相应的分数及次数
        user_bias_score = {}
        user_appearance_count = {}
        # 文件夹路径
        folder_path = rf"F:\three_parts_output\external_url\output_{month}"
        # 遍历文件夹下所有以-output.csv结尾的文件
        for filename in os.listdir(folder_path):
            if filename.endswith("-output.csv"):
                file_path = os.path.join(folder_path, filename)
                df = pd.read_csv(file_path, usecols=['retweeted_user_id', 'retweet_expanded_urls_array'],
                                 dtype={'retweeted_user_id': 'str', 'retweet_expanded_urls_array': 'str'})
                print('正在处理：', file_path)
                for index, row in df.iterrows():
                    user_id = row['retweeted_user_id']
                    urls = row['retweet_expanded_urls_array'].split(',')  # 分隔多个URL
                    first_url = urls[0].strip()  # 只取第一条URL，并去除首尾空格
                    domain = extract_domain(first_url).lower()  # 提取域名并转换为小写
                    score = url_score.get(domain)  # 使用get方法获取分数，若不存在则返回None

                    if score is not None:  # 仅当domain存在于url_score时继续执行
                        if user_id in user_bias_score:
                            user_bias_score[user_id] += score
                            user_appearance_count[user_id] += 1
                        else:
                            user_bias_score[user_id] = score
                            user_appearance_count[user_id] = 1

        # 将两个字典合并到一个DataFrame中
        user_stats = pd.DataFrame({
            'user_id': list(user_bias_score.keys()),
            'total_score': list(user_bias_score.values()),
            'appearance_count': list(user_appearance_count.values())
        })

        # 保存每个月的结果为CSV文件
        output_path = rf"F:\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating\user_bias_scores_{month}.csv"
        user_stats.to_csv(output_path, index=False)

        # 将每个月的数据累计到总体数据中
        for user_id in user_bias_score:
            if user_id in overall_user_bias_score:
                overall_user_bias_score[user_id] += user_bias_score[user_id]
                overall_user_appearance_count[user_id] += user_appearance_count[user_id]
            else:
                overall_user_bias_score[user_id] = user_bias_score[user_id]
                overall_user_appearance_count[user_id] = user_appearance_count[user_id]

        # 最后将所有月份的数据汇总并保存为CSV文件
    overall_user_stats = pd.DataFrame({
        'user_id': list(overall_user_bias_score.keys()),
        'total_score': list(overall_user_bias_score.values()),
        'appearance_count': list(overall_user_appearance_count.values())
    })

    overall_output_path = r"F:\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating\user_bias_scores_overall.csv"
    overall_user_stats.to_csv(overall_output_path, index=False)


if __name__ == '__main__':
    user_bias_by_media()


    # # # 调用函数并打印结果来检查url标签和url-bias映射的字典
    # file_path = r"F:\Experimental Results\media-bias-final-url-cleaned.csv"
    # url_score_dict = build_url_score_dict(file_path)
    # print(url_score_dict)




    # 清洗url标签
    # file_path = 'F:\\Experimental Results\\media-only-url-bias-final-url.csv'
    # output_file_path = 'F:\\Experimental Results\\media-bias-final-url-cleaned.csv'
    #
    # df = pd.read_csv(file_path, usecols=['domain', 'bias'], dtype={'domain': 'str', 'bias': 'str'})
    #
    # # 清洗bias列标签
    # df_cleaned = clean_bias_labels(df)
    #
    # # 重新统计清洗后的bias类别计数
    # bias_counts_cleaned = df_cleaned['bias'].value_counts()
    #
    # print("Cleaned Bias Category Counts in CSV:")
    # for bias, count in bias_counts_cleaned.items():
    #     print(f"{bias}: {count} entries")
    #
    # # 保存清洗后的文件
    # df_cleaned.to_csv(output_file_path, index=False)
    # print(f"Cleaned file saved to {output_file_path}")


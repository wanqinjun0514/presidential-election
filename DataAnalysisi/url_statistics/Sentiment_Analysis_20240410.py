import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import os
import glob
from transformers import pipeline
import gc
import shutil
#读取\us-presidential-output下的所有以-output.csv结尾的文件retweeted_full_text字段，把每一行的retweeted_full_text字段都输入到postive_negative_neutral_compound函数里，将每一行的retweeted_id字段、retweet_id字段、retweeted_full_text字段经过postive_negative_neutral_compound函数算出的compound的值，这三个字段保存到一个新的csv文件里，文件名命名成原来文件名-compound.csv（原文件名去掉-output）
def postive_negative_neutral_compound():
    month = '2020_01'
    directory_path = fr"G:\us-presidential-output\output_{month}"
    # 新目录的名称
    new_directory_name = f"retweeted_full_text_compound_{month}"
    # 在当前脚本运行的目录中创建新目录
    new_directory_path = os.path.join(r'G:\retweeted_full_text_compound', new_directory_name)
    os.makedirs(new_directory_path, exist_ok=True)  # 如果目录不存在，则创建它
    # 查找所有以-output.csv结尾的文件
    csv_files = glob.glob(os.path.join(directory_path, "*-output.csv"))
    # 为了避免重复下载VADER的词汇集，我们先下载一次
    nltk.download('vader_lexicon')
    # 创建VADER的情感强度分析器
    sia = SentimentIntensityAnalyzer()
    print("VADER的词汇集下载完成。")

    # 定义一个内部函数来处理单个文本，并返回compound值
    def calculate_compound(text):
        # 检查文本是否为字符串类型
        if not isinstance(text, str):
            # 如果不是字符串，可以选择返回0（中性情感）
            return 0
        return sia.polarity_scores(text)['compound']

    # 处理每个文件
    for file_path in csv_files:
        df = pd.read_csv(file_path, dtype={'retweet_id': str, 'retweeted_id': str, 'retweeted_full_text': str},
                        usecols=['retweet_id', 'retweeted_id', 'retweeted_full_text'])
        print("正在处理文件：", file_path)
        # 使用VADER分析文本情感  计算compound值
        df['compound'] = df['retweeted_full_text'].apply(calculate_compound)  # 返回一个字典包含四个键：neg（负面情感分数）、neu（中性情感分数）、pos（正面情感分数）和compound（综合情感分数）。compound分数可以用来快速判断文本的总体情感倾向：正值通常表示正面情感，负值表示负面情感，而接近零则可能表示中性情感。
        # 创建新的文件名
        new_file_name = os.path.basename(file_path).replace("-output.csv", "-compound.csv")
        new_file_path = os.path.join(new_directory_path, new_file_name)
        # 保存到新的CSV文件
        df[['retweeted_id', 'retweet_id', 'compound']].to_csv(new_file_path, index=False)
        print("计算了VADER的情感强度后，新文件保存在：", new_file_path)

def eight_emotions_classfiy111():
    month = '2020_01'
    directory_path = fr"H:\us-presidential-output\output_{month}"
    # 新目录的名称
    new_directory_name = f"retweeted_full_text_eight_emotions_classfiy_{month}"
    # 在当前脚本运行的目录中创建新目录
    new_directory_path = os.path.join(r'G:\retweeted_full_eight_emotions_classfiy', new_directory_name)
    os.makedirs(new_directory_path, exist_ok=True)  # 如果目录不存在，则创建它
    # 查找所有以-output.csv结尾的文件
    csv_files = glob.glob(os.path.join(directory_path, "*-output.csv"))
    classifier = pipeline('text-classification', model='bhadresh-savani/distilbert-base-uncased-emotion',
                          top_k=None)  # return_all_scores=True参数已被弃用
    # 定义一个内部函数来处理单个文本，并返回compound值
    def calculate_emotion(text):
        # 检查文本是否为字符串类型
        if not isinstance(text, str):
            # 如果不是字符串，可以选择返回0（中性情感）
            return 0
        result = classifier(text)
        # 检查结果是否为非空的嵌套列表
        if result and isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
            max_score = -1
            max_label = 'neutral'
            for item in result[0]:
                if item['score'] > max_score:
                    max_score = item['score']
                    max_label = item['label']
            print(max_label,max_score)
            return max_label, max_score

        return 'neutral', 0.0  # 如果结果不符合预期，返回默认值
    # 处理每个文件
    for file_path in csv_files:
        df = pd.read_csv(file_path, dtype={'retweet_id': str, 'retweeted_id': str, 'retweeted_full_text': str},
                         usecols=['retweet_id', 'retweeted_id', 'retweeted_full_text'])
        print("正在处理文件：", file_path)
        # 划分NRC情感词典里的八种基本情感 进行情绪分析
        df['emotion'], df['score'] = df['retweeted_full_text'].apply(
            calculate_emotion)  # 返回一个字典包含四个键：neg（负面情感分数）、neu（中性情感分数）、pos（正面情感分数）和compound（综合情感分数）。compound分数可以用来快速判断文本的总体情感倾向：正值通常表示正面情感，负值表示负面情感，而接近零则可能表示中性情感。
        # 创建新的文件名
        new_file_name = os.path.basename(file_path).replace("-output.csv", "-eight_emotions_classfiy.csv")
        new_file_path = os.path.join(new_directory_path, new_file_name)
        # 保存到新的CSV文件
        df[['retweeted_id', 'retweet_id', 'emotion', 'score']].to_csv(new_file_path, index=False)
        print("划分了八种基本情感后，新文件保存在：", new_file_path)



# def eight_emotions_classfiy():
#     month = '2020_01'
#     # directory_path = fr"H:\original_fulltext_and_tweet_id\original_fulltext_and_tweet_id_with_languages\drop_duplicate"
#     directory_path = fr"H:\original_fulltext_and_tweet_id\original_fulltext_and_tweet_id_with_languages\drop_duplicate"
#
#     # 新目录的名称
#     new_directory_name = f"retweeted_full_text_eight_emotions_classfiy_{month}"
#     # 在当前脚本运行的目录中创建新目录
#     new_directory_path = os.path.join(r'H:\retweeted_full_eight_emotions_classfiy', new_directory_name)
#     os.makedirs(new_directory_path, exist_ok=True)  # 如果目录不存在，则创建它
#     # 查找所有以-output.csv结尾的文件
#     csv_files = glob.glob(os.path.join(directory_path, f"*{month}_with_languages.csv"))
#     print(csv_files)
#     classifier = pipeline('text-classification', model='bhadresh-savani/distilbert-base-uncased-emotion',
#                           top_k=None)  # return_all_scores=True参数已被弃用
#
#     # 定义一个内部函数来处理单个文本，并返回情感和得分
#     def calculate_emotion(text):
#         # 检查文本是否为字符串类型
#         if not isinstance(text, str):
#             # 如果不是字符串，可以选择返回'neutral'和0.0（中性情感）
#             return 'neutral', 0.0
#         result = classifier(text)
#         # 检查结果是否为非空的嵌套列表
#         if result and isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
#             max_score = -1
#             max_label = 'neutral'
#             for item in result[0]:
#                 if item['score'] > max_score:
#                     max_score = item['score']
#                     max_label = item['label']
#             print(max_label, max_score)
#             return max_label, max_score
#
#         return 'neutral', 0.0  # 如果结果不符合预期，返回默认值
#
#     # 处理每个文件
#     for file_path in csv_files:
#         df = pd.read_csv(file_path, dtype={'retweet_id': str, 'retweeted_origin_full_text': str},
#                          usecols=['retweet_id', 'retweeted_origin_full_text'])
#         print("正在处理文件：", file_path)
#
#         # 划分NRC情感词典里的八种基本情感 进行情绪分析
#         # emotions_scores = df['retweeted_full_text'].apply(calculate_emotion)
#         emotions_scores = df['retweeted_origin_full_text'].apply(calculate_emotion)
#
#         df['emotion'] = emotions_scores.apply(lambda x: x[0])
#         df['score'] = emotions_scores.apply(lambda x: x[1])
#
#         # 创建新的文件名
#         new_file_name = os.path.basename(file_path).replace("_with_languages.csv", f"{month}-eight_emotions_classfiy.csv")
#         new_file_path = os.path.join(new_directory_path, new_file_name)
#         # 保存到新的CSV文件
#         df[['retweet_id', 'emotion', 'score']].to_csv(new_file_path, index=False)
#         print("划分了八种基本情感后，新文件保存在：", new_file_path)

def eight_emotions_classfiy():
    month = '2020_07'
    directory_path = fr"H:\original_fulltext_and_tweet_id\original_fulltext_and_tweet_id_with_languages\drop_duplicate"

    new_directory_name = f"retweeted_full_text_eight_emotions_classify_{month}"
    new_directory_path = os.path.join(r'H:\retweeted_full_eight_emotions_classify', new_directory_name)
    os.makedirs(new_directory_path, exist_ok=True)

    csv_files = glob.glob(os.path.join(directory_path, f"*{month}_with_languages.csv"))
    print(csv_files)

    classifier = pipeline('text-classification', model='bhadresh-savani/distilbert-base-uncased-emotion', top_k=None)

    def truncate_text(text, max_length=512):
        if not isinstance(text, str):
            return text
        return text[:max_length]

    def calculate_emotion(text):
        if not isinstance(text, str):
            return 'neutral', 0.0
        text = truncate_text(text)
        result = classifier(text)
        if result and isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
            max_score = -1
            max_label = 'neutral'
            for item in result[0]:
                if item['score'] > max_score:
                    max_score = item['score']
                    max_label = item['label']
            return max_label, max_score
        return 'neutral', 0.0

    start_index = 0  # 从第五万条数据开始
    save_interval = 10000  # 每处理一万条数据保存一次

    for file_path in csv_files:
        df = pd.read_csv(file_path, dtype={'retweet_id': str, 'retweeted_origin_full_text': str},
                         usecols=['retweet_id', 'retweeted_origin_full_text'])
        print("正在处理文件：", file_path)

        for index in range(start_index, len(df)):
            row = df.iloc[index]
            emotion, score = calculate_emotion(row['retweeted_origin_full_text'])
            df.at[index, 'emotion'] = emotion
            df.at[index, 'score'] = score

            if (index + 1) % save_interval == 0 or index == len(df) - 1:
                new_file_name = os.path.basename(file_path).replace("_with_languages.csv",
                                                                    f"_{month}-eight_emotions_classify_part{(index + 1) // save_interval}.csv")
                new_file_path = os.path.join(new_directory_path, new_file_name)
                # 保存数据，追加模式
                if os.path.exists(new_file_path):
                    df.iloc[start_index:index + 1][['retweet_id', 'emotion', 'score']].to_csv(new_file_path, mode='a',
                                                                                              header=False, index=False)
                else:
                    df.iloc[start_index:index + 1][['retweet_id', 'emotion', 'score']].to_csv(new_file_path,
                                                                                              index=False)
                print(f"保存记录 {index + 1}/{len(df)} 到文件：{new_file_path}")
                start_index = index + 1
                # 释放内存
                del row
                gc.collect()
        del df # 最后释放内存
        gc.collect()

if __name__ == "__main__":
    # postive_negative_neutral_compound()
    eight_emotions_classfiy()
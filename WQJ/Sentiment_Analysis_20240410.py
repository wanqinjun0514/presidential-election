import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import os
import glob
#读取\us-presidential-output下的所有以-output.csv结尾的文件retweeted_full_text字段，把每一行的retweeted_full_text字段都输入到postive_negative_neutral_compound函数里，将每一行的retweeted_id字段、retweet_id字段、retweeted_full_text字段经过postive_negative_neutral_compound函数算出的compound的值，这三个字段保存到一个新的csv文件里，文件名命名成原来文件名-compound.csv（原文件名去掉-output）
def postive_negative_neutral_compound():
    directory_path = r"G:\us-presidential-output\2019-12-test_extract"
    # 查找所有以-output.csv结尾的文件
    csv_files = glob.glob(os.path.join(directory_path, "*-output.csv"))
    # 为了避免重复下载VADER的词汇集，我们先下载一次
    nltk.download('vader_lexicon')
    # 创建VADER的情感强度分析器
    sia = SentimentIntensityAnalyzer()
    print("VADER的词汇集下载完成。")

    # 定义一个内部函数来处理单个文本，并返回compound值
    def calculate_compound(text):
        return sia.polarity_scores(text)['compound']

    # 处理每个文件
    for file_path in csv_files:
        df = pd.read_csv(file_path, dtype={'retweet_id': str})  # 读取CSV文件
        print("正在处理文件：", file_path)
        # 使用VADER分析文本情感  计算compound值
        df['compound'] = df['retweeted_full_text'].apply(calculate_compound)  # 返回一个字典包含四个键：neg（负面情感分数）、neu（中性情感分数）、pos（正面情感分数）和compound（综合情感分数）。compound分数可以用来快速判断文本的总体情感倾向：正值通常表示正面情感，负值表示负面情感，而接近零则可能表示中性情感。
        # 创建新的文件名
        new_file_name = os.path.basename(file_path).replace("-output.csv", "-compound.csv")
        new_file_path = os.path.join(directory_path, new_file_name)
        # 保存到新的CSV文件
        df[['retweeted_id', 'retweet_id', 'compound']].to_csv(new_file_path, index=False)
        print("计算了VADER的情感强度后，新文件保存在：", new_file_path)



if __name__ == "__main__":
    postive_negative_neutral_compound()
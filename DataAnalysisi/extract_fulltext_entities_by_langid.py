import langid
import pandas as pd
import os
#对full text的处理步骤是提取所有原推文的fulltext-原推文id的映射
def extract_mapping_of_original_fulltext_and_tweet_id_and_retweet_id():
    dates = [
        '2019_12', '2020_01', '2020_02', '2020_03', '2020_04',
             '2020_05', '2020_06', '2020_07', '2020_08', '2020_09',
             '2020_10', '2020_11', '2020_12',
             '2021_01', '2021_02', ]

    for date in dates:
        directory_path = fr'H:\us-presidential-output\output_{date}'
        result_path = rf'H:\original_fulltext_and_tweet_id\combined_original_fulltext_and_tweet_id_{date}.csv'
        combined_data = pd.DataFrame()  # 创建一个空的DataFrame来存储合并的数据
        # 遍历指定目录下的所有文件
        for filename in os.listdir(directory_path):
            if filename.endswith('.csv'):  # 确保处理的是CSV文件
                file_path = os.path.join(directory_path, filename)  # 获取完整的文件路径
                print('正在处理：', file_path)
                try:
                    # 读取CSV文件
                    data = pd.read_csv(file_path, dtype=str, usecols=['retweeted_origin_full_text', 'retweet_id'])
                    # 过滤掉任何空值的行
                    data.dropna(subset=['retweeted_origin_full_text', 'retweet_id'], inplace=True)
                    # 将读取的数据添加到combined_data DataFrame中
                    combined_data = pd.concat([combined_data, data])
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
        # 将合并后的数据保存到新的CSV文件中
        combined_data.to_csv(os.path.join(directory_path, result_path), index=False)
        print(directory_path, '文件夹中的所有文件处理完毕，将结果保存在了：', result_path)


# def langid_judge_languages():
#     # 假设你有一个包含文本的DataFrame # 创建DataFrame，确保文本被包含在列表中
#     df = pd.DataFrame({'text': ["FLASHBACK: MORE Classified Material Found on Hillary Clinton's Email Server, thanks to @JudicialWatch heavy lifting--@RealDonaldTrump should ask where's the DOJ?  https://t.co/9Br5kzsLPB https://t.co/waHhEPU0u2"]})
#     # 应用langid来识别语言
#     df['language'] = df['text'].apply(langid.classify)
#     # 提取语言代码
#     df['language_code'] = df['language'].apply(lambda x: x[0])
#     print(df)

def langid_judge_languages(input_file_path, output_file_path):
    try:
        # 读取CSV文件，确保包括 'retweet_id' 和 'retweeted_origin_full_text'
        df = pd.read_csv(input_file_path, usecols=['retweet_id', 'retweeted_origin_full_text'])

        # 使用langid来识别每行文本的语言，并创建新的列 'language'
        df['language'] = df['retweeted_origin_full_text'].apply(
            lambda x: langid.classify(x)[0] if pd.notnull(x) else None)

        # 保存扩展后的DataFrame到新的CSV文件
        df.to_csv(output_file_path, index=False)
        print("File saved successfully with additional 'language' column.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # extract_mapping_of_original_fulltext_and_tweet_id_and_retweet_id()
    dates = [
        '2019_12', '2020_01', '2020_02', '2020_03', '2020_04',
             '2020_05', '2020_06', '2020_07', '2020_08', '2020_09',
             '2020_10', '2020_11', '2020_12',
             '2021_01', '2021_02', ]
    for date in dates:
        input_file_path = fr'H:\original_fulltext_and_tweet_id\combined_original_fulltext_and_tweet_id_{date}.csv'
        output_file_path = fr'H:\original_fulltext_and_tweet_id\original_fulltext_and_tweet_id_with_languages\combined_original_fulltext_and_tweet_id_{date}_with_languages.csv'
        langid_judge_languages(input_file_path, output_file_path)
    # langid_judge_languages()
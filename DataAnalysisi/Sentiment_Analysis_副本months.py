
import pandas as pd
import os
import glob
from transformers import pipeline
import gc
def eight_emotions_classfiy():
    month = '2020_02'
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
        del df  # 最后释放内存
        gc.collect()

if __name__ == "__main__":
    eight_emotions_classfiy()
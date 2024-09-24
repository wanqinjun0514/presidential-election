import pandas as pd
import os
import openpyxl

# 将所有旧数据的被转发的用户id补充完整
def match_all_old_data_tweetid_with_userid():
    # 设置pandas以避免科学计数法，确保长数字正确显示
    pd.set_option('display.float_format', lambda x: '%.0f' % x)
    # 读取包含表头的total_merge_df
    total_merge_df = pd.read_excel('H:\\old_data\\total_tweet_id_to_user_id_1216_with_newandold_matched.xlsx', header=0, names=['tweet_id','user_id'])
    # 创建字典
    tweet_id_to_user_id = {str(row['tweet_id']): str(row['user_id']) for index, row in total_merge_df.iterrows()}
    folder_path = r'F:\2020_US_presidential_election\page4\page4-separation02'
    # 遍历目标文件夹中的所有以_output.xlsx结尾的文件
    for file in os.listdir(folder_path):
        if file.endswith("_output.xlsx"):
            print("正在读取文件：", file)
            file_path = os.path.join(folder_path, file)
            try:
                wb = openpyxl.load_workbook(file_path, data_only=True)
                ws = wb.active
                for row in ws.iter_rows(min_row=1):  # min_row=2假设第一行是表头  没有表头
                    tweet_id = str(row[3].value)  # 第四列的值
                    if tweet_id:  # 检查tweet_id是否存在
                        tweet_id_str = str(tweet_id)
                        if tweet_id_str in tweet_id_to_user_id:
                            row[2].value = tweet_id_to_user_id[tweet_id_str]  # 只更新第三列的值
                        else:
                            row[2].value = None  # 如果没有匹配，则清除第三列的值
                # 保存文件
                wb.save(file_path)
                # 保存文件
                print("匹配后保存文件：", file)
            except Exception as e:
                print(f"处理文件 {file} 时出错: {e}")





if __name__ == "__main__":

    match_all_old_data_tweetid_with_userid()
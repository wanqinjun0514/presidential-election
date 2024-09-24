import os
from langdetect import detect, LangDetectException
import pandas as pd
import spacy
#
#
#
# for i in range(1,3):
#     output_folder = f'H:\\us-presidential-output\\2021-{i}'
#
#     if not os.path.exists(output_folder):
#         # 如果不存在，创建文件夹
#         os.makedirs(output_folder)
#         print(f"Folder '{output_folder}' created.")
#     else:
#         print(f"Folder '{output_folder}' already exists.")

#
# # 替换为你的CSV文件路径
# csv_path = 'H:\\demo_data\\2019-12-01-1-output.csv'
# # csv_path = "H:\\us-presidential-output\\output_2019_12\\2019-12-01-1-output.csv"
# # 使用pandas读取CSV文件
# df = pd.read_csv(csv_path, header=0, dtype=str, escapechar="\\")
#
#
# print(len(df))
# print(df)
# # 计算DataFrame长度的一半
# # half_len = len(df) // 2
#
# # 保留前一半的数据
# # df_first_half = df.iloc[:half_len]
#
# # 显示保留的数据的前几行以确认
# # print(df_first_half)
#
# # # 如果需要，可以将修改后的DataFrame保存回CSV文件
# # df_first_half.to_csv(csv_path, index=False)
#
#
# # Replace all internal line breaks in the DataFrame with a space
# cleaned_df = df.replace(to_replace=r'\r\n|\n|\r', value=' ', regex=True)
#
# # Write the cleaned DataFrame to a new CSV file
# # cleaned_df.to_csv(csv_path, index=False)
# import pandas as pd
#
# # # 将提供的数据行分割并计算字段数量
# # data_line = ""
# # fields = data_line.split(',')
# # num_fields = len(fields)
# # print(num_fields)
#
# csv_path = "H:\\state\\merge-NLP\\2020-02.csv"
# df_csv = pd.read_csv(csv_path, header=0,
#                      dtype={'retweeted_user_id': 'str', 'retweeted_user_location': 'str', 'Count': 'int', 'entities': 'str'})
#
# print(df_csv['entities'].count())
#
# print(detect("冬がいちばん似合う街"))

# csv_path = f"H:\\state\\location-NlP\\none_entities_in_states.csv"
# result_path = f"H:\\state\\location-NlP\\none_entities_in_states-1.csv"
#
# # 读取数据
# print("开始读取！")
# df_csv = pd.read_csv(csv_path, header=0,dtype={'Location': 'str', 'Count': 'int', 'entities': 'str', 'language': 'str'})
# print("读取完成！")
# print(df_csv)
# np_csv = df_csv.to_numpy()
# print(np_csv)
# print("转换完成")
#
# entities_list = []
# lang_list = []
# nlp = spacy.load('en_core_web_lg')
#
# # 迭代 DataFrame 中的每一行
# for data in np_csv:
#     # print(data)
#     loc = data[0]
#     ent = data[2]
#     lang = data[3]
#     if pd.isna(ent):
#         # print(loc)
#         try:
#             doc = nlp(loc)  # 使用NLP模型处理位置文本
#             entities = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
#             if entities:  # 检查是否找到了实体
#                 entities_list.append(entities)
#                 lang = 'en'  # 设置语言为英语
#             else:
#                 entities_list.append(None)  # 如果没有找到实体，则添加None
#         except Exception as e:  # 通用异常处理
#             print(f"Error processing location: {loc}, Error: {e}")
#             entities_list.append(None)  # 如果处理失败，则添加None
#
#     else:
#         entities_list.append(ent)  # 如果原始数据中已有实体数据，直接复制过来
#     lang_list.append(lang)  # 更新语言列表
#
#
# # 将命名实体列表添加为 DataFrame 的一个新列
# df_csv['entities'] = entities_list
# df_csv['language'] = lang_list  # 更新 DataFrame 的语言列
# # # 现在可以查看 DataFrame，或将其保存回 CSV
# print(df_csv)
# df_csv.to_csv(result_path, index=False, header=True)

# loc_list = [('Lagos', 0, 5, 'LOC'), ('Nigeria', 7, 14, 'LOC')]
#
# for loc_tuple in loc_list:
#     print(loc_tuple[0])

# # 加载 Spacy 模型
# nlp = spacy.load('en_core_web_lg')
#
# string = "It was nice of Trump to give Red State Governors a break from covering up coronavirus deaths with covering up policy brutality. @realDonaldTrump"
#
# doc = nlp(string)
# entities = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
# print(entities)
#
# import numpy as np
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
# import matplotlib.pyplot as plt
#
# # 示例数据集
# data = np.array([
#     [2.5, 2.4],
#     [0.5, 0.7],
#     [2.2, 2.9],
#     [1.9, 2.2],
#     [3.1, 3.0],
#     [2.3, 2.7],
#     [2, 1.6],
#     [1, 1.1],
#     [1.5, 1.6],
#     [1.1, 0.9]
# ])
#
# # 数据标准化
# scaler = StandardScaler()
# scaled_data = scaler.fit_transform(data)
#
# # 计算PCA
# pca = PCA(n_components=2)  # 保留2个主成分
# principal_components = pca.fit_transform(scaled_data)
#
# # 打印主成分和解释方差
# print("主成分：")
# print(pca.components_)
# print("解释方差：")
# print(pca.explained_variance_ratio_)
#
# # 可视化主成分
# plt.figure()
# plt.scatter(principal_components[:, 0], principal_components[:, 1])
# plt.xlabel('Principal Component 1')
# plt.ylabel('Principal Component 2')
# plt.title('PCA Result')
# plt.show()


# import plotly.express as px
# import pandas as pd
#
# # 示例数据
# data = {
#     'A': [1, 2, 3, 4, 5],
#     'B': [5, 4, 3, 2, 1],
#     'C': [10, 20, 30, 40, 50],
#     'D': [100, 200, 300, 400, 500]
# }
# df = pd.DataFrame(data)
#
# fig = px.scatter_3d(df, x='A', y='B', z='C', color='D', size='D', size_max=40,
#                     title='3D Scatter Plot with Four Variables')
# fig.update_layout(scene = dict(
#                     xaxis_title='Variable A',
#                     yaxis_title='Variable B',
#                     zaxis_title='Variable C'))
#
# # 保存为HTML文件
# fig.write_html('H:\\d_scatter_plot.html')
# fig.show()



output_path = 'H:\\geo-bias\\ervery_mouth_every_state_bias_num_proportion.csv'  # 替换为你的输出文件路径
df = pd.read_csv(output_path, header=0)
state = df['State'].unique()
times = df['Month'].unique()

print(state)
print(type(state), len(state))
print(times)
print(len(times))

print(53*15)

select_df = df[df['Interval'] == '[-3, -2.5)']
print(select_df)
select_df1 = select_df[select_df['Count'] != 0]
print(select_df1)



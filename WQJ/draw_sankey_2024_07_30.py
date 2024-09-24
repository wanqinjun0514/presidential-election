import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go

folder_path = f"F:\\us-presidential-output\\politician_average_rating\\without_url-rating"
all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

# 空列表，用于存储每个文件的DataFrame
data_frames = []

for file in all_files:
    df = pd.read_csv(file)
    # 只保留需要的列
    df = df[['retweeted_user_id', 'average_bias_points']]
    # 提取月份和年份，假设文件名格式为"YYYY_MM_output.csv"
    df['year_month'] = file.split('/')[-1].split('_output.csv')[0]
    data_frames.append(df)

# 合并所有DataFrame
combined_df = pd.concat(data_frames, ignore_index=True)

def convert_bias_points(value):
    if value <= -1/3:
        return -1
    elif value < 1/3:
        return 0
    else:
        return 1

combined_df['average_bias_points'] = combined_df['average_bias_points'].apply(convert_bias_points)

# 按用户和日期排序
combined_df.sort_values(by=['retweeted_user_id', 'year_month'], inplace=True)

# 确保输出文件夹存在
output_dir = f"F:\\us-presidential-output\\politician_average_rating\\without_url-rating\\sankey"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 获取所有独特的月份，按顺序排列
unique_months = sorted(combined_df['year_month'].unique())

# 为每两个连续的月份绘制桑基图
for i in range(len(unique_months) - 1):
    # 筛选当前两个月的数据
    current_data = combined_df[
        (combined_df['year_month'] == unique_months[i]) | (combined_df['year_month'] == unique_months[i + 1])]

    # 为当前两个月创建数据连接
    current_data['next_bias_points'] = current_data.groupby('retweeted_user_id')['average_bias_points'].shift(-1)
    current_data.dropna(subset=['next_bias_points'], inplace=True)  # 删除 NaN 值
    current_data['next_bias_points'] = current_data['next_bias_points'].astype(int)

    # 计算变化频率
    change_frequency = current_data.groupby(['average_bias_points', 'next_bias_points']).size().reset_index(
        name='count')

    # 桑基图的节点和链接
    nodes = [{'name': str(i)} for i in range(-1, 2)]
    links = [{'source': int(x[0]), 'target': int(x[1]) + 3, 'value': int(x[2])} for x in change_frequency.values]

    # 绘制桑基图
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=[f'{unique_months[i]}: {x["name"]}' for x in nodes] + [f'{unique_months[i + 1]}: {x["name"]}' for x in
                                                                         nodes],
        ),
        link=dict(

            source=[l['source'] for l in links],
            target=[l['target'] for l in links],
            value=[l['value'] for l in links]
        ))])

    fig.update_layout(title_text=f"Changes in User Bias Points from {unique_months[i]} to {unique_months[i + 1]}",
                      font_size=10)

    # 保存为 PNG 图像
    fig.write_image(f"{output_dir}/Sankey_{unique_months[i]}_to_{unique_months[i + 1]}.png")
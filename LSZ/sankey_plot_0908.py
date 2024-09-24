import pandas as pd
import plotly.graph_objects as go
import os
import re

#让我们接着前面的数据处理继续，对于每一个形如common_user_bias_2019_12_to_2020_01.csv的文件，我们都做如下处理：
# 对于每个retweeted_user_id所对应的两个average，我们将[-1,0)视为Left，0视为Center，(0,1]视为Right。绘制每个csv文件中的桑基图，即left center right到left center right的转移。展示绘制的图（总共14张）。

# 输入文件夹路径
input_folder = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\external_url-rating\sankey_plot\common_user_bias'


# 类别分类函数
def categorize_bias(bias):
    if bias < 0:
        return 'Left'
    elif bias == 0:
        return 'Center'
    else:
        return 'Right'


# 更新颜色映射为美观的RGB颜色
node_color_map = {
    'Left': 'rgb(052, 073, 100)',  # 深蓝色
    'Center': 'rgb(240, 245, 182)',  # 亮黄色
    'Right': 'rgb(210, 077, 083)',  # 深红色
    'DEFAULT': 'rgb(200, 200, 200)'  # 默认灰色
}

# 连边颜色映射
link_color_map = {
    'Left': 'rgba(177, 217, 299, 0.5)',  # 浅蓝色，半透明
    'Center': 'rgba(250, 252, 228, 0.9)',  # 浅黄色，半透明
    'Right': 'rgba(245, 186, 186, 0.5)',  # 浅红色，半透明
    'DEFAULT': 'rgba(200, 200, 200, 0.5)'  # 默认灰色，半透明
}

# 获取所有 common_user_bias_YYYY_MM_to_YYYY_MM.csv 文件
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# 处理每个文件并生成桑基图
for csv_file in csv_files:
    file_path = os.path.join(input_folder, csv_file)

    # 读取数据
    df = pd.read_csv(file_path)

    # 将两个月的 average_bias_points 进行分类
    df['month1_category'] = df['average_bias_points_month1'].apply(categorize_bias)
    df['month2_category'] = df['average_bias_points_month2'].apply(categorize_bias)

    # 统计从一个类别到另一个类别的转换
    transition_counts = df.groupby(['month1_category', 'month2_category']).size().reset_index(name='count')

    # 桑基图的标签
    labels = ['Left', 'Center', 'Right']

    # 创建 source 和 target 列表
    source = []
    target = []
    values = []
    link_colors = []  # 用于存储连边的颜色

    # 生成source, target 和 value 列表
    for _, row in transition_counts.iterrows():
        source_label = row['month1_category']
        target_label = row['month2_category']

        source.append(labels.index(source_label))
        target.append(labels.index(target_label) + len(labels))  # target需要偏移位置
        values.append(row['count'])

        # 设置连边颜色
        link_colors.append(link_color_map.get(source_label, link_color_map['DEFAULT']))

    # 创建桑基图
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels + labels,  # 前一列是source，后一列是target
            color=[node_color_map.get(label, node_color_map['DEFAULT']) for label in labels + labels]  # 设置节点颜色
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color=link_colors  # 设置连边颜色
        )
    ))

    # 更新布局并展示图表
    fig.update_layout(title_text=f'Sankey Diagram for {csv_file[:-4]}', font_size=10)
    fig.show()  # 展示图表

# 批量重命名newplot.png
def change_name():
    # 文件夹路径
    folder_path = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\twitter_url-rating\sankey_plot\Sankey_plot\month'

    # 目标文件名列表
    new_filenames = [
        "common_user_bias_2019_12_to_2020_01.png",
        "common_user_bias_2020_01_to_2020_02.png",
        "common_user_bias_2020_02_to_2020_03.png",
        "common_user_bias_2020_03_to_2020_04.png",
        "common_user_bias_2020_04_to_2020_05.png",
        "common_user_bias_2020_05_to_2020_06.png",
        "common_user_bias_2020_06_to_2020_07.png",
        "common_user_bias_2020_07_to_2020_08.png",
        "common_user_bias_2020_08_to_2020_09.png",
        "common_user_bias_2020_09_to_2020_10.png",
        "common_user_bias_2020_10_to_2020_11.png",
        "common_user_bias_2020_11_to_2020_12.png",
        "common_user_bias_2020_12_to_2021_01.png",
        "common_user_bias_2021_01_to_2021_02.png"
    ]

    # 获取文件名中的数字编号并排序的函数
    def extract_file_number(filename):
        # 匹配形如 "newplot (1).png" 或 "newplot.png" 的文件
        match = re.search(r'newplot(?: \((\d+)\))?.png', filename)
        if match:
            return int(match.group(1)) if match.group(1) else 0
        return -1

    # 获取当前文件夹下所有图片文件
    image_files = [f for f in os.listdir(folder_path) if f.startswith('newplot') and f.endswith('.png')]

    # 按文件名中的编号对文件进行排序
    image_files_sorted = sorted(image_files, key=extract_file_number)

    # 确保文件数量一致
    if len(image_files_sorted) != len(new_filenames):
        print("文件数量不匹配，请检查文件夹中的图片数量。")
    else:
        # 按顺序重命名文件
        for i, image_file in enumerate(image_files_sorted):
            old_path = os.path.join(folder_path, image_file)
            new_path = os.path.join(folder_path, new_filenames[i])
            os.rename(old_path, new_path)
            print(f'Renamed {image_file} to {new_filenames[i]}')

    print("重命名完成！")


change_name()
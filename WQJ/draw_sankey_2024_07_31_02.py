import pandas as pd
import os
import plotly.graph_objects as go


def plot_multi_columns_sankey_by_meida():
    start_month = 201912
    end_month = 202102

    # 生成所有月份组合的列表
    month_pairs = []
    current_year = start_month // 100
    current_month = start_month % 100

    while current_year * 100 + current_month < end_month:
        next_year = current_year
        next_month = current_month + 1
        if next_month > 12:
            next_month = 1
            next_year += 1

        # 生成年_月的格式
        current_month_str = f"{current_year}_{current_month:02d}"
        next_month_str = f"{next_year}_{next_month:02d}"

        # 添加到列表中，但仅当下个月不超过结束月份
        if next_year * 100 + next_month <= end_month:
            month_pairs.append((current_month_str, next_month_str))

        current_year, current_month = next_year, next_month

    print(month_pairs)

    # 初始化一个空的长格式DataFrame来存储所有数据
    long_df = pd.DataFrame()

    for month_pair in month_pairs:
        # 构造每个CSV文件的路径
        # csv_file = rf"F:\Experimental Results\Average_Bias_Rating\politician_average_rating\twitter_url-rating\every_month\cross_table\transitions_sankey_{month_pair[0]}_to_{month_pair[1]}.csv"
        # csv_file = rf"F:\Experimental Results\Average_Bias_Rating\politician_average_rating\external_url-rating\every_month\cross_table\transitions_sankey_{month_pair[0]}_to_{month_pair[1]}.csv"

        csv_file = rf"F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\every_month\cross_table\transitions_sankey_{month_pair[0]}_to_{month_pair[1]}.csv"


        temp_df = pd.read_csv(csv_file)
        # 确保列名是统一的
        temp_df.columns = ['source', 'target', 'value']
        # 添加到长格式DataFrame
        long_df = pd.concat([long_df, temp_df], ignore_index=True)

    # 处理节点和连边颜色
    nodes = list(set(long_df['source']).union(set(long_df['target'])))
    node_dict = {node: i for i, node in enumerate(nodes)}

    # 定义节点和连边颜色
    node_color_map = {
        'Left': 'rgb(51, 102, 153)',
        'Center': 'rgb(240, 230, 140)',
        'Right': 'rgb(204, 102, 102)',
        'DEFAULT': 'rgb(128, 128, 128)'
    }

    def extract_color_suffix(node_name):
        if 'Left' in node_name:
            return 'Left'
        elif 'Center' in node_name:
            return 'Center'
        elif 'Right' in node_name:
            return 'Right'
        else:
            return 'DEFAULT'

    node_colors = [node_color_map[extract_color_suffix(node)] for node in nodes]

    link_color_map = {suffix: f"rgba{color[3:-1]},0.5)" for suffix, color in
                      node_color_map.items()}  # Using RGBA for transparency
    link_colors = [link_color_map[extract_color_suffix(long_df.iloc[i]['source'])] for i in range(len(long_df))]

    # 创建桑基图数据
    link = {
        'source': long_df['source'].map(node_dict).astype(int),
        'target': long_df['target'].map(node_dict).astype(int),
        'value': long_df['value'],
        'color': link_colors
    }

    # 创建桑基图
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=list(node_dict.keys()),
            color=node_colors
        ),
        link=link
    )])

    # 更新布局并显示
    fig.update_layout(title_text="Multi-Month User Bias Flow Sankey Diagram", font_size=10)

    # 在显示之前设置图表的下载和编辑功能
    config = {'toImageButtonOptions': {
        'format': 'svg',  # 支持 png, svg, jpeg, webp
        'filename': 'custom_image',
        'height': 700,
        'width': 900,
        'scale': 1  # 缩放比例 (只对raster格式有效)
    }}

    fig.show(config=config)

plot_multi_columns_sankey_by_meida()
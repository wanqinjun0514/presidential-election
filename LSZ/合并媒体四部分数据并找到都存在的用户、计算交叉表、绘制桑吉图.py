import pandas as pd
import glob
import os
import plotly.graph_objects as go


# 帮我读取F:\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating下以quarterly_user_bias_scores_开头的csv，每个csv的表头都是user_id,total_score,appearance_count,average_bias_points
# 读取每个季度的用户数据，我想从六个季度的数据里找到六个季度都存在的用户user_id，以及这些相同的用户id对应的每个季度的average_bias_points保存下来，存在一个新的csv里，新csv的表头可以是user_id,2019_12_2020_01_2020_02_average_bias_points,2020_03_2020_04_2020_05_average_bias_points,2020_06_2020_07_2020_08_average_bias_points,2020_09_2020_10_average_bias_points,2020_11_2020_12_average_bias_points,2021_01_2021_02_average_bias_points
def 找到所有季度里都存在的用户():
    # 设置文件目录路径
    dir_path = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\user_bias_scores_by_quarter'

    # 获取所有匹配的CSV文件列表
    file_pattern = os.path.join(dir_path, 'quarterly_user_bias_scores_*.csv')
    file_list = glob.glob(file_pattern)

    # 存储季度信息和文件路径的列表
    quarter_data = []

    for file_path in file_list:
        filename = os.path.basename(file_path)
        # 从文件名中提取季度名称
        quarter_name = filename[len('quarterly_user_bias_scores_'):-len('.csv')]
        # 创建对应的列名
        column_name = quarter_name + '_average_bias_points'
        quarter_data.append((quarter_name, column_name, file_path))

    # 按季度名称排序，确保顺序正确
    quarter_data.sort()

    # 初始化数据框列表和列名列表
    data_frames = []
    quarter_column_names = []

    # 读取每个CSV文件并处理数据
    for quarter_name, column_name, file_path in quarter_data:
        df = pd.read_csv(file_path, encoding='utf-8')
        df = df[['user_id', 'average_bias_points']]
        df.rename(columns={'average_bias_points': column_name}, inplace=True)
        data_frames.append(df)
        quarter_column_names.append(column_name)

    # 合并所有数据框，取所有季度都存在的用户
    merged_df = data_frames[0]
    for df in data_frames[1:]:
        merged_df = pd.merge(merged_df, df, on='user_id', how='inner')

    # 指定输出的列顺序
    output_columns = ['user_id'] + quarter_column_names
    merged_df = merged_df[output_columns]

    save_path = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\sankey_plot\all_quarters'

    # 将结果保存到新的CSV文件中
    output_file = os.path.join(save_path, 'all_quaters_common_users_merged_user_average_bias_points.csv')
    merged_df.to_csv(output_file, index=False, encoding='utf-8')

    print("数据处理完成，结果已保存到：", output_file)



# 对每个季度的平均分数做分类，分类函数等会在categorize_bias里提供给你，分类完之后要统计出每个季度每种分类的个数有多少个
def 统计所有季度的各类政治倾向用户的数量():
    # 读取合并后的CSV文件
    df = pd.read_csv(
        r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\sankey_plot\all_quarters\all_quaters_common_users_merged_user_average_bias_points.csv',
        encoding='utf-8')

    # 列出所有季度的列名
    quarters = [
        '2019_12_2020_01_2020_02_average_bias_points',
        '2020_03_2020_04_2020_05_average_bias_points',
        '2020_06_2020_07_2020_08_average_bias_points',
        '2020_09_2020_10_average_bias_points',
        '2020_11_2020_12_average_bias_points',
        '2021_01_2021_02_average_bias_points'
    ]

    # 定义一个函数，根据average_bias_points的值进行分类
    def categorize_bias(score):
        if -3 <= score < -2.5:
            return 'Extreme bias Left'
        elif -2.5 <= score < -1.5:
            return 'Left'
        elif -1.5 <= score < -0.5:
            return 'Left leaning'
        elif -0.5 <= score < 0.5:
            return 'Center'
        elif 0.5 <= score < 1.5:
            return 'Right leaning'
        elif 1.5 <= score < 2.5:
            return 'Right'
        elif 2.5 <= score <= 3:
            return 'Extreme bias Right'
        else:
            return 'Unknown'

    # 定义所有可能的类别
    categories = [
        'Extreme bias Left',
        'Left',
        'Left leaning',
        'Center',
        'Right leaning',
        'Right',
        'Extreme bias Right',
        'Unknown'
    ]

    # 为每个季度的列应用分类函数
    for quarter in quarters:
        df[quarter + '_category'] = df[quarter].apply(categorize_bias)

    # 构建统计结果的DataFrame
    category_counts_list = []

    for quarter in quarters:
        category_col = quarter + '_category'
        counts = df[category_col].value_counts()
        # 确保所有类别都在列中，如果没有则填充为0
        counts = counts.reindex(categories, fill_value=0)
        total = counts.sum()
        counts['季度总和'] = total
        # 去除 '_average_bias_points' 后缀，使季度名称更简洁
        quarter_name = quarter.replace('_average_bias_points', '')
        counts.name = quarter_name
        category_counts_list.append(counts)

    # 将列表转换为DataFrame
    category_counts_df = pd.DataFrame(category_counts_list)

    # 重置索引，将季度作为第一列
    category_counts_df.reset_index(inplace=True)
    category_counts_df.rename(columns={'index': 'Quarter'}, inplace=True)

    # 重新排列列的顺序
    columns_order = ['Quarter'] + categories + ['季度总和']
    category_counts_df = category_counts_df[columns_order]

    # 保存统计结果到CSV文件
    output_path = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\sankey_plot\all_quarters\category_counts.csv'
    category_counts_df.to_csv(output_path, index=False, encoding='utf-8')


# 已检查 交叉表数据没有问题
def 构建所有季度的政治倾向转移交叉表():
    # 读取CSV文件
    file_path = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\sankey_plot\all_quarters\all_quaters_common_users_merged_user_average_bias_points.csv'
    df = pd.read_csv(file_path)

    # 定义区间和标签
    bins = [-3, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3]
    labels = ['Extreme bias Left', 'Left', 'Left leaning', 'Center', 'Right leaning', 'Right', 'Extreme bias right']

    # 定义一个函数来分类政治倾向
    def categorize_bias(score):
        if -3 <= score < -2.5:
            return 'Extreme bias Left'
        elif -2.5 <= score < -1.5:
            return 'Left'
        elif -1.5 <= score < -0.5:
            return 'Left leaning'
        elif -0.5 <= score < 0.5:
            return 'Center'
        elif 0.5 <= score < 1.5:
            return 'Right leaning'
        elif 1.5 <= score < 2.5:
            return 'Right'
        elif 2.5 <= score <= 3:
            return 'Extreme bias right'
        else:
            return 'Unknown'  # 处理任何不在[-3, 3]范围内的值

    # 处理每个季度的数据
    columns = [
        '2019_12_2020_01_2020_02_average_bias_points',
        '2020_03_2020_04_2020_05_average_bias_points',
        '2020_06_2020_07_2020_08_average_bias_points',
        '2020_09_2020_10_average_bias_points',
        '2020_11_2020_12_average_bias_points',
        '2021_01_2021_02_average_bias_points'
    ]

    # 为每个季度生成政治倾向分类
    for col in columns:
        df[f'category_{col}'] = df[col].apply(categorize_bias)

    # 初始化一个空列表存储所有季度之间的转换
    all_transitions_data = []

    # 遍历所有相邻季度的转移
    for i in range(len(columns) - 1):
        col1 = f'category_{columns[i]}'
        col2 = f'category_{columns[i + 1]}'

        # 初始化每个季度之间的转换字典
        transitions = {f'{l1} to {l2}': 0 for l1 in labels for l2 in labels}

        # 计算类别间的转换
        for _, row in df.iterrows():
            transitions[f'{row[col1]} to {row[col2]}'] += 1

        # 构建这个季度之间的转换数据
        for k, v in transitions.items():
            source, target = k.split(' to ')
            all_transitions_data.append({
                'source': f'{columns[i]}_{source}',
                'target': f'{columns[i + 1]}_{target}',
                'value': v
            })

    # 将所有季度的转换数据保存为CSV文件
    all_transitions_df = pd.DataFrame(all_transitions_data)
    output_path = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\sankey_plot\all_quarters\all_quaters_users_transitions_sankey.csv'
    all_transitions_df.to_csv(output_path, index=False)


def 绘制多栏桑基图():
    csv_file = rf'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\sankey_plot\all_quarters\all_quaters_users_transitions_sankey.csv'
    df = pd.read_csv(csv_file)
    # 定义列名
    col_names = ['source', 'target', 'value']
    # 初始化空的DataFrame来存储转换后的数据
    long_df = pd.DataFrame()
    for i in range(0, df.shape[1], 3):
        # 临时DataFrame，处理每个时间段的数据
        temp_df = pd.DataFrame(df.iloc[:, i:i + 3].values, columns=col_names)
        # 添加到长格式DataFrame
        long_df = pd.concat([long_df, temp_df])
    # 重置索引
    long_df.reset_index(drop=True, inplace=True)
    # 接下来，绘制桑基图：
    # 获取所有唯一的节点
    nodes = list(set(long_df['source']).union(set(long_df['target'])))
    # 节点映射到数字ID，因为Plotly的Sankey图需要用数字ID来表示节点
    node_dict = {node: i for i, node in enumerate(nodes)}

    # 定义一个函数，用于从节点名称中提取颜色关键字
    def extract_color_suffix(node_name):
        if 'Extreme bias Left' in node_name:
            return 'Extreme bias Left'
        elif 'Left leaning' in node_name:
            return 'Left leaning'
        elif 'Left' in node_name:
            return 'Left'
        elif 'Center' in node_name:
            return 'Center'
        elif 'Right leaning' in node_name:
            return 'Right leaning'
        elif 'Right' in node_name:
            return 'Right'
        elif 'Extreme bias right' in node_name:
            return 'Extreme bias right'
        else:
            return 'DEFAULT'  # 对于不匹配任何关键字的节点，返回一个默认值

    # 节点颜色映射
    node_color_map = {
        'Extreme bias Left': 'rgb(0, 51, 102)',  # 最深蓝色
        'Left': 'rgb(51, 102, 153)',  # 深蓝色
        'Left leaning': 'rgb(181, 216, 243)',  # 中等蓝色
        'Center': 'rgb(240, 230, 140)',  # 浅黄色
        'Right leaning': 'rgb(255, 153, 153)',  # 浅红色
        'Right': 'rgb(204, 102, 102)',  # 中等红色
        'Extreme bias right': 'rgb(139, 26, 26)',  # 深红色
        'DEFAULT': 'rgb(128, 128, 128)'  # 默认灰色，用于不匹配的情况
    }

    # 连边颜色映射，颜色与节点颜色相似但更透明
    link_color_map = {
        'Extreme bias Left': 'rgba(0, 51, 102, 0.5)',  # 最深蓝色，半透明
        'Left': 'rgba(51, 102, 153, 0.5)',  # 深蓝色，半透明
        'Left leaning': 'rgba(181, 216, 243, 0.5)',  # 中等蓝色，半透明
        'Center': 'rgba(240, 230, 140, 0.7)',  # 浅黄色，稍透明
        'Right leaning': 'rgba(255, 153, 153, 0.5)',  # 浅红色，半透明
        'Right': 'rgba(204, 102, 102, 0.5)',  # 中等红色，半透明
        'Extreme bias right': 'rgba(139, 26, 26, 0.5)',  # 深红色，半透明
        'DEFAULT': 'rgb(128, 128, 128)'  # 默认灰色，用于不匹配的情况
    }

    # 使用上面定义的函数为每个节点分配颜色
    node_colors = [node_color_map[extract_color_suffix(node)] for node in nodes]  # 设置连边颜色
    # 对于连边颜色，我们需要查找每个连边的源节点，并据此确定颜色
    link_colors = [link_color_map[extract_color_suffix(long_df.iloc[i]['source'])] for i in range(len(long_df))]

    # 创建桑基图数据
    link = {
        'source': long_df['source'].map(node_dict).astype(int),
        'target': long_df['target'].map(node_dict).astype(int),
        'value': long_df['value'],
        'color': link_colors  # 设置连边颜色
    }

    # 创建桑基图
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=[node for node in node_dict],
            color=node_colors  # 设置节点颜色
        ),
        link=link
    )])

    # 更新布局并显示
    fig.update_layout(title_text="Time Series Sankey Diagram", font_size=10)
    fig.show()



if __name__ == '__main__':
    # 找到所有季度里都存在的用户()
    # 统计所有季度的各类政治倾向用户的数量()
    # 构建所有季度的政治倾向转移交叉表()
    绘制多栏桑基图()
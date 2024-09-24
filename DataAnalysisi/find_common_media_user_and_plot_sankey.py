import pandas as pd
import os
import plotly.graph_objects as go


# 用python实现对G:\with_url_data\without_twitter_top_200_user_id_bias\matching_top_200_user_id_2019_12.csv文件进行数据统计。
# csv文件有表头（retweeted_user_id,Domain,bias）三列数据，用usercols只读取retweeted_user_id和bias列
# 先将bias列的数据都转换成数字：Extreme bias right转换成3，Right是2，Right leaning是1，Center是0，Left leaning是-1，Left是-2，其他的数据也是0。
# 转换成数字之后，需要统计每个retweeted_user_id的用户出现的次数和该retweeted_user_id用户的bias列的总和，最后计算出每个retweeted_user_id的用户的平均值（bias总和除以出现的次数）
# 将这四列数据保存在新的csv文件里（retweeted_user_id、bias列的总和、出现次数、平均值）
def user_bias_by_meida():
    # 更改为实际的文件路径
    date = '2020_11'
    file_path = rf"H:\with_url_data\without_twitter_top_200_user_id_bias\retweet_user_id_Domain_bias\matching_top_200_user_id_{date}.csv"
    output_path = rf"H:\with_url_data\without_twitter_top_200_user_id_bias\media_user_bias_{date}-DEMO.csv"
    # 读取CSV文件，只包括'retweeted_user_id'和'bias'列
    df = pd.read_csv(file_path, usecols=['retweeted_user_id', 'bias'], dtype={'retweeted_user_id': 'str', 'Domain': 'str', 'bias': 'str'})
    print(df['retweeted_user_id'].dtype)
    # 定义转换规则
    bias_mapping = {
        'Extreme bias right': 3,
        'Right': 2,
        'Right leaning': 1,
        'Center': 0,
        'Left leaning': -1,
        'Left': -2
    }

    # 默认值为0，不在字典中的任何其他值也将被转换为0
    df['bias'] = df['bias'].apply(lambda x: bias_mapping.get(x, 0))

    # 统计每个'retweeted_user_id'的出现次数和bias总和
    user_stats = df.groupby('retweeted_user_id')['bias'].agg(['count', 'sum'])
    user_stats['average'] = user_stats['sum'] / user_stats['count']

    # 重置索引以将'retweeted_user_id'作为列而不是索引
    user_stats.reset_index(inplace=True)

    # 重命名列以匹配要求的输出格式
    user_stats.columns = ['retweeted_user_id', 'count', 'sum', 'average']
    # 对DataFrame按照average列进行排序
    user_stats = user_stats.sort_values(by='average')
    # 保存到新的CSV文件
    user_stats.to_csv(output_path, index=False)


# 每两个月之间相同用户id的bias平均值拼接在一个csv文件里
def find_common_user_between_two_months_by_media():
    date1 = '2020_10'
    date2 = '2020_11'
    # 文件路径
    path1 = rf'H:\with_url_data\without_twitter_top_200_user_id_bias\media_user_bias_score\media_user_bias_{date1}.csv'
    path2 = rf'H:\with_url_data\without_twitter_top_200_user_id_bias\media_user_bias_score\media_user_bias_{date2}.csv'

    # 读取文件
    df1 = pd.read_csv(path1, usecols=['retweeted_user_id', 'average'],
                      dtype={'retweeted_user_id': 'str', 'average': 'float64'})
    df2 = pd.read_csv(path2, usecols=['retweeted_user_id', 'average'],
                      dtype={'retweeted_user_id': 'str', 'average': 'float64'})

    # 更改列名以区分
    df1.rename(columns={'average': 'date1_average'}, inplace=True)
    df2.rename(columns={'average': 'date2_average'}, inplace=True)

    # 设置显示选项
    pd.set_option('display.max_columns', None)  # 不限制列数
    pd.set_option('display.width', None)  # 根据内容自动调整输出宽度

    print(df1)
    print(df2)
    print("-" * 500)

    common_ids1 = pd.merge(df1[['retweeted_user_id']], df2[['retweeted_user_id']], on='retweeted_user_id')
    print(common_ids1)
    print("-" * 500)

    common_ids2 = df1[df1['retweeted_user_id'].isin(df2['retweeted_user_id'])]
    print(common_ids2)
    print("-" * 500)

    # 合并数据
    merged_df = pd.merge(df1, df2, on='retweeted_user_id')
    print(merged_df)
    # # 保存新的CSV文件
    output_path = rf'G:\with_url_data\without_twitter_top_200_user_id_bias\every_month\merged_media_user_bias_{date1}_to{date2}.csv'
    merged_df.to_csv(output_path, index=False)


# 统计构建媒体数据对用户观念影响的桑基图的矩阵数据
# 从上一个月的七类政治倾向变化到下一个月的七类政治倾向的桑基图  矩阵数据是7*7的，保存到csv文件里
def Construct_matrix_data_for_drawing_Sankey_diagrams_by_media():
    # 文件路径设置
    date1 = '2021_01'
    date2 = '2021_02'
    # 载入数据
    file_path = f"G:/with_url_data/without_twitter_top_200_user_id_bias/every_month/merged_media_user_bias_{date1}_to{date2}.csv"
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

    # 应用函数到数据列
    df['category_2019'] = df['date1_average'].apply(categorize_bias)
    df['category_2020'] = df['date2_average'].apply(categorize_bias)
    # 统计每个类别的数量
    count_2019_12 = df['category_2019'].value_counts()
    count_2020_01 = df['category_2020'].value_counts()
    # 初始化转换字典
    transitions = {f'{l1} to {l2}': 0 for l1 in labels for l2 in labels}
    # 计算类别间的转换
    for _, row in df.iterrows():
        transitions[f'{row["category_2019"]} to {row["category_2020"]}'] += 1
    # 打印每个类别的数量和转换情况
    print('date1的各区间数量:', count_2019_12)
    print('date2的各区间数量:', count_2020_01)
    for k, v in transitions.items():
        print(f'{k}: {v}')
    # 将转换数据保存到CSV
    transitions_data = []
    for k, v in transitions.items():
        source, target = k.split(' to ')
        transitions_data.append({
            'source': f'{date1}_{source}',
            'target': f'{date2}_{target}',
            'value': v
        })
    transitions_df = pd.DataFrame(transitions_data)
    transitions_df.to_csv(
        rf"G:\with_url_data\without_twitter_top_200_user_id_bias\every_month\cross_table\transitions_sankey_{date1}_to_{date2}.csv",
        index=False)


# 根据G:\with_url_data\without_twitter_top_200_user_id_bias\every_month\cross_table\transitions_sankey_2019_12_to_2020_01.csv每个月份的交叉表绘制桑基图
def plot_monthly_sankey_by_meida():
    # 一个月与下一个月之间的相同用户：
    # 一个季度与下一个季度之间的相同用户：
    date1 = '2019_12'
    date2 = '2020_05'
    csv_file = rf'G:\with_url_data\without_twitter_top_200_user_id_bias\every_month\combined_multi_columns_sankey_data\merged_transitions_sankey_{date1}_to_{date2}.csv'
    df = pd.read_csv(csv_file)
    df.columns = ['source', 'target', 'value']  # 假设CSV文件有标题
    # 预定义节点顺序
    nodes = [
        f'{date1}_Extreme bias Left', f'{date1}_Left', f'{date1}_Left leaning', f'{date1}_Center',
        f'{date1}_Right leaning', f'{date1}_Right', f'{date1}_Extreme bias right',
        f'{date2}_Extreme bias Left', f'{date2}_Left', f'{date2}_Left leaning', f'{date2}_Center',
        f'{date2}_Right leaning', f'{date2}_Right', f'{date2}_Extreme bias right'
    ]

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
    node_colors = [node_color_map[extract_color_suffix(node)] for node in nodes]

    # 对于连边颜色，我们需要查找每个连边的源节点，并据此确定颜色
    link_colors = [link_color_map[extract_color_suffix(link['source'])] for _, link in df.iterrows()]

    # 创建桑基图数据
    link = {
        'source': df['source'].map(node_dict).astype(int),
        'target': df['target'].map(node_dict).astype(int),
        'value': df['value'],
        'color': link_colors  # 设置连边颜色
    }
    # 创建桑基图
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=nodes,
            color=node_colors  # 设置节点颜色
        ),
        link=link
    )])

    # 更新布局并显示
    fig.update_layout(title_text="Time Series Sankey Diagram", font_size=10)
    fig.show()


def plot_multi_columns_sankey_by_meida():
    date1 = '2020_10'
    date2 = '2021_02'
    csv_file = rf'G:\with_url_data\without_twitter_top_200_user_id_bias\every_month\combined_multi_columns_sankey_data\merged_transitions_sankey_{date1}_to_{date2}.csv'
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


def cheak_repetition_line():
    floder1 = rf'H:\with_url_data\without_twitter_top_200_user_id_bias\media_user_bias_score'
    csv_name = os.listdir(floder1)

    for name in csv_name:
        print("-------------------------------------------------------------------------------------------------------")
        print(name)
        cvs_path = os.path.join("H:\\with_url_data\\without_twitter_top_200_user_id_bias\\media_user_bias_score", name)
        # print(cvs_path)

        df = pd.read_csv(cvs_path, usecols=['retweeted_user_id', 'average'],
                         dtype={'retweeted_user_id': 'str', 'average': 'float64'})

        # 设置显示选项
        pd.set_option('display.max_columns', None)  # 不限制列数
        pd.set_option('display.width', None)  # 根据内容自动调整输出宽度

        # print(df)

        duplicates = df.duplicated(subset=['retweeted_user_id'])
        if duplicates.any():
            print("df存在重复行")
            print(duplicates)
            print(df[duplicates])
        else:
            print("df没有重复行")



if __name__ == "__main__":
    # find_common_user_between_two_months_by_media()
    # Construct_matrix_data_for_drawing_Sankey_diagrams_by_media()
    # plot_monthly_sankey_by_meida()
    # plot_multi_columns_sankey_by_meida()

    # cheak_repetition_line()

    # user_bias_by_meida()

    df = pd.read_csv("H:\\with_url_data\\without_twitter_top_200_user_id_bias\\media_user_bias_2020_11-DEMO.csv", usecols=['retweeted_user_id', 'average'],
                     dtype={'retweeted_user_id': 'str', 'average': 'float64'})

    # 设置显示选项
    pd.set_option('display.max_columns', None)  # 不限制列数
    pd.set_option('display.width', None)  # 根据内容自动调整输出宽度

    # print(df)

    duplicates = df.duplicated(subset=['retweeted_user_id'])
    if duplicates.any():
        print("df存在重复行")
        print(duplicates)
        print(df[duplicates])
    else:
        print("df没有重复行")

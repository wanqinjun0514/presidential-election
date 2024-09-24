import csv
import glob
import pandas as pd
import os
import plotly.graph_objects as go
import numpy as np


# 根据用户id找到用户名。
# 具体步骤是：
# 读取G:\record\count_user_id_record\origin_retweet_user下的total-count-origin-user-id.csv文件（有表头，第一列叫value，第二列叫count。其中第一列是用户id，第二列是计数），读取该csv的前2000个用户id，对用户id构建字典，key值为用户id，value为用户名，初始化value都为空值
# 然后根据用户id去G:\us-presidential-output\merge_2019_12\2019-12-01-1-output.csv匹配用户名并且最后把用户id和用户名保存在新的csv文件里。
# 需要注意这个2019-12-01-1-output.csv文件我可能还会替换，如果前2000个用户id有的用户id没有匹配到用户名，我会替换这个csv文件去其他的csv文件里对没有匹配到用户名的用户id再找，直到所有前2000个用户id都找到了用户名
def match_and_save_user_names(user_ids_csv_path, data_csv_paths, output_csv_path, limit=2000):
    # 读取用户ID
    user_ids = []
    with open(user_ids_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i >= limit:
                break
            user_ids.append(row['Value'])
    # 初始化用户名字典
    user_names = {user_id: '' for user_id in user_ids}

    # 遍历CSV文件匹配用户名
    for data_csv_path in data_csv_paths:
        print(f"正在从文件 {data_csv_path} 中查找用户名...")
        try:
            with open(data_csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                # 确保必要的列名存在
                if 'retweet_origin_user_id' not in reader.fieldnames or 'retweet_origin_username' not in reader.fieldnames:
                    print(f"文件 {data_csv_path} 中缺少必要的列名，跳过此文件。")
                    continue
                next(reader)  # Skip header
                for row in reader:
                    user_id = row['retweet_origin_user_id']  # 使用列名访问用户ID  # retweet_origin_user_id
                    user_name = row['retweet_origin_username']  # 使用列名访问用户名  # retweet_origin_username
                    if user_id in user_names and not user_names[user_id]:
                        user_names[user_id] = user_name
                        # print(f"为用户ID {user_id} 找到了用户名: {user_name}")
            # 检查是否所有用户ID都已找到用户名
        except csv.Error as e:
            print(f"处理文件 {data_csv_path} 时遇到错误: {e}，跳过此文件。")
            continue
    if all(name for name in user_names.values()):
        print("已为所有用户ID找到用户名。")
    else:
        missing_ids = [user_id for user_id, user_name in user_names.items() if not user_name]
        print(f"警告：以下用户ID的用户名未找到：{missing_ids}")
    # 保存结果
    with open(output_csv_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['user_id', 'user_name'])
        for user_id, user_name in user_names.items():
            writer.writerow([user_id, user_name])


#
# 具体步骤：读取到G:\us-presidential-output下的所有以merge_20开头的文件夹下的所有以-output.csv结尾的文件的路径赋值给data_csv_paths
def find_csv_paths():
    # 查找所有满足条件的CSV文件路径
    root_dir = 'G:\\us-presidential-output'
    folder_prefix = 'merge_20'
    file_suffix = '-output.csv'
    # 构建搜索模式以匹配指定前缀的文件夹下的指定后缀的文件
    pattern = f"{root_dir}\\{folder_prefix}*\\*{file_suffix}"
    # 使用glob.glob查找匹配的文件路径
    return glob.glob(pattern)


# 匹配用户名的时候漏掉了count，补充上
# 具体步骤：把matched_origin_retweet_user_names_top2000.csv里补充上total-count-origin-user-id.csv文件里的Count字段，具体步骤：读取G:\record\count_user_id_record\origin_retweet_user\total-count-origin-user-id.csv文件，该文件有表头Value和Count，matched_origin_retweet_user_names_top2000.csv文件有表头user_id和user_name，根据user_id和Value匹配上了话就把count补充到matched_origin_retweet_user_names_top2000.csv里
def match_count():
    # 读取CSV文件
    total_count_df = pd.read_csv('G:/record/count_user_id_record/origin_retweet_user/total-count-origin-user-id.csv')
    matched_df = pd.read_csv(
        'G:/record/count_user_id_record/origin_retweet_user/matched_origin_retweet_user_names_top2000.csv')

    # 根据user_id和Value合并两个数据帧，假设user_id对应于Value
    merged_df = pd.merge(matched_df, total_count_df, left_on='user_id', right_on='Value', how='left')

    # 删除多余的Value列（如果需要）
    merged_df.drop(columns=['Value'], inplace=True)

    # 保存到新的CSV文件
    merged_df.to_csv(
        'G:/record/count_user_id_record/origin_retweet_user/updated_matched_origin_retweet_user_names_top2000.csv',
        index=False)

    print("文件已更新并保存。")


# 根据用户id匹配用户的bias
# 具体步骤：把matched_origin_retweet_user_names_with_count_top100.csv里补充上political_figure_20240404.xlsx里的political_bias字段，该xlsx文件的表头是id和political_bias。csv文件的表头是user_id和user_name和Count，这些都不变，根据csv里的user_id和xlsx文件的id进行匹配，匹配上了话就把political_bias补充到csv里
def match_political_bias():
    # 读取CSV文件
    csv_file_path = r'G:\record\count_user_id_record\origin_retweet_user\matched_origin_retweet_user_names_with_count_top100.csv'
    csv_df = pd.read_csv(csv_file_path)

    # 读取Excel文件
    excel_file_path = r'G:\旧数据\political_figure_20240404.xlsx'
    excel_df = pd.read_excel(excel_file_path)

    # 根据user_id和id合并两个数据帧
    merged_df = pd.merge(csv_df, excel_df, left_on='user_id', right_on='id', how='left')

    # 删除多余的id列（如果需要）
    merged_df.drop(columns=['id'], inplace=True)

    # 保存到新的CSV文件
    new_csv_file_path = r'G:\record\count_user_id_record\origin_retweet_user\updated_matched_origin_retweet_user_names_with_count_top100.csv'
    merged_df.to_csv(new_csv_file_path, index=False)
    print("文件已更新并保存。")


# 计算转帖用户的政治倾向分数总和、平均分数
# 具体步骤：
# - 根据G:\record\count_user_id_record\origin_retweet_user\matched_origin_retweet_user_names_with_count_with_bias_top100.csv（表头分别是：user_id,user_name,Count,political_bias），构建出user_id和political_bias转换成分数的字典，key值为user_id，value为political_bias分数（需要将political_bias字符转换成可以统计的数字，political_bias只有三类字符，即：LEFT算为-2，CENTER算成0，RIGHT算成2）。
# - 初始化两个字典，第一个字典是retweeted_user_id和总分数的映射（总分数初始值为0），第二个字典是retweeted_user_id和其出现次数的映射（其出现次数初始值为0）
# - 然后读取在G:\us-presidential-output\merge_2019_12文件夹下所有以-output.csv命名结尾的csv文件（有表头），一行行处理，如果某行的retweet_origin_user_id字段出现在user_id和political_bias分数的字典里，就把该行的retweeted_user_id字段保存到retweeted_user_id和总分数的字典的里，key值为retweeted_user_id，value为political_bias分数到累加value里，并且把retweeted_user_id和其出现次数的映射里的出现次数也加一
# - 最终保存到一个csv里，有四列数据：retweeted_user_id、bias总分、retweeted_user_id出现次数、平均值（该平均值是由bias总分除以retweeted_user_id出现次数）
def count_monthly_retweet_user_bias():
    # Step 1: Read the CSV and Create a Dictionary for Political Bias Scores
    # Load the CSV file
    df_bias = pd.read_csv(
        'G:\\record\\count_user_id_record\\origin_retweet_user\\matched_origin_retweet_user_names_with_count_with_bias_top100.csv')
    # Map political biases to scores
    bias_to_score = {'LEFT': -2, 'CENTER': 0, 'RIGHT': 2}
    # Create a dictionary with user_id as keys and political bias scores as values
    user_bias_scores = {row['user_id']: bias_to_score[row['political_bias']] for index, row in df_bias.iterrows()}

    # Step 2: Initialize Two Dictionaries for Total Scores and Counts
    total_scores = {}
    count_occurrences = {}

    # Step 3: Process CSV Files and Update Dictionaries
    # Path where your CSV files are located
    path = 'G:\\us-presidential-output\\merge_2020_01'  # 修改每个月份的文件路径
    result_path = 'G:\\record\\retweet_user_bias\\merge_2020_01_retweet_user_bias.csv'
    all_files = glob.glob(os.path.join(path, '*-output.csv'))
    for file in all_files:
        df = pd.read_csv(file)
        print('正在处理文件：', file)
        for index, row in df.iterrows():
            origin_user_id = row['retweet_origin_user_id']
            retweeted_user_id = row['retweeted_user_id']
            if origin_user_id in user_bias_scores:
                # Update total_scores dictionary
                if retweeted_user_id not in total_scores:
                    total_scores[retweeted_user_id] = 0
                total_scores[retweeted_user_id] += user_bias_scores[origin_user_id]

                # Update count_occurrences dictionary
                if retweeted_user_id not in count_occurrences:
                    count_occurrences[retweeted_user_id] = 0
                count_occurrences[retweeted_user_id] += 1

    # Step 4: Calculate Averages and Save to CSV
    # Prepare the data for the new CSV
    data_for_csv = []
    for user_id, total_score in total_scores.items():
        count = count_occurrences[user_id]
        average_score = total_score / count
        data_for_csv.append({'retweeted_user_id': user_id, 'bias_total_score': total_score, 'occurrences': count,
                             'average_score': average_score})

    # Convert to DataFrame and save to CSV
    df_final = pd.DataFrame(data_for_csv)
    df_final.to_csv(result_path, index=False)


# 找到相同的用户id并把用户观念平均分做区间划分，最后绘制桑基图
# 具体步骤：
# 找到相同的用户id和两个月份的用户观念平均值：merge_2019_12_retweet_user_bias.csv、merge_2020_01_retweet_user_bias.csv，都有表头（分别是：retweeted_user_id,bias_total_score,occurrences,average_score），我需要从这两个csv文件里找到相同的retweeted_user_id并且分别把2019_12_average_score和2020_01average_score，保存在新的一个csv里
# 读取这个新生成的相同用户id及其观念平均值变化的CSV文件，计算2019_12_average_score和2020_01_average_score的平均值变化，变化将根据提供的区间[-2, -0.5]、[-0.5, 0.5]、[0.5, 2]来分类
# 输出3*3的矩阵，即行是：在csv_file的2019_12_average_score列里统计出[-2, -0.5)、[-0.5, 0.5)、[0.5, 2]的数量，列是在csv_file的2020_01_average_score列里统计出[-2, -0.5)、[-0.5, 0.5)、[0.5, 2]的数量
# 将矩阵转换成便于作为桑基图输入的csv文件
# 最后绘制桑基图
def find_common_user_within_two_months_and_plot_sankey():
    # 读取CSV文件
    date1 = '2021_01'
    date2 = '2021_02'
    # # 使用f-string来插入变量值
    df_2019_12 = pd.read_csv(fr'G:\record\retweet_user_bias\merge_{date1}_retweet_user_bias.csv',
                             usecols=['retweeted_user_id', 'average_score'])
    df_2020_01 = pd.read_csv(fr'G:\record\retweet_user_bias\merge_{date2}_retweet_user_bias.csv',
                             usecols=['retweeted_user_id', 'average_score'])
    # 重命名列以区分两个文件
    df_2019_12.rename(columns={'average_score': f'{date1}_average_score'}, inplace=True)
    df_2020_01.rename(columns={'average_score': f'{date2}_average_score'}, inplace=True)
    # 合并两个DataFrame，基于'retweeted_user_id'
    common_retweeted_user_id_csv_file = fr'G:\record\retweet_user_bias\merged_average_scores_{date1}-{date2}.csv'
    merged_df = pd.merge(df_2019_12, df_2020_01, on='retweeted_user_id')
    # 保存到新的CSV文件
    merged_df.to_csv(common_retweeted_user_id_csv_file, index=False)
    print('相同用户id及其观念平均值变化文件已保存在：', common_retweeted_user_id_csv_file)
    # 计算交叉表（3*3的矩阵）
    df = pd.read_csv(common_retweeted_user_id_csv_file)
    # 定义区间
    bins = [-2, -0.5, 0.5, 2]
    # 计算每个区间的数量
    df[f'{date1}_range'] = pd.cut(df[f'{date1}_average_score'], bins=bins, right=False, include_lowest=True,
                                  labels=['[-2, -0.5)', '[-0.5, 0.5)', '[0.5, 2]'])
    df[f'{date2}_range'] = pd.cut(df[f'{date2}_average_score'], bins=bins, right=False, include_lowest=True,
                                  labels=['[-2, -0.5)', '[-0.5, 0.5)', '[0.5, 2]'])
    # 利用pandas的交叉表（crosstab）功能来创建这样一个矩阵，并且它会自带行和列的标签
    # 使用pd.crosstab()生成交叉表
    ct = pd.crosstab(df[f'{date1}_range'], df[f'{date2}_range'])
    # 输出结果
    print('相同用户id及其观念平均值变化矩阵：\n', ct)

    # 将矩阵转换成csv文件
    # 修改列名和行索引前，先定义一个映射关系来替换表达方式
    mapping = {
        '[-2, -0.5)': '_LEFT',
        '[-0.5, 0.5)': '_CENTER',
        '[0.5, 2]': '_RIGHT'
    }
    # 应用映射关系修改列名和行索引
    ct.columns = [f'{date2}{mapping[col]}' for col in ct.columns]
    ct.index = [f'{date1}{mapping[idx]}' for idx in ct.index]
    # 将交叉表转换为需要的格式的DataFrame
    data = {'source': [], 'target': [], 'value': []}
    for source, row in ct.iterrows():
        for target, value in row.items():
            data['source'].append(source)
            data['target'].append(target)
            data['value'].append(value)

    result_df = pd.DataFrame(data)
    # 保存到CSV
    result_df.to_csv(fr'G:\record\retweet_user_bias\formatted_cross_tab_result_{date1}_to_{date2}.csv', index=False)
    # 打印DataFrame以确认内容
    print(result_df)

    # 绘制桑基图
    # 提取节点
    nodes = set(result_df['source']).union(set(result_df['target']))
    # 节点映射到数字ID，Plotly的Sankey图需要用数字来指代节点
    node_dict = {node: i for i, node in enumerate(nodes)}
    # 构造桑基图所需的数据结构
    link = {
        'source': result_df['source'].map(node_dict),
        'target': result_df['target'].map(node_dict),
        'value': result_df['value']
    }
    # 创建桑基图
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,  # 节点间的间距
            thickness=20,  # 节点的厚度
            line=dict(color='black', width=0.5),
            label=list(nodes),  # 节点标签
        ),
        link=link  # 链接信息
    )])
    # 设置图表的标题
    fig.update_layout(title_text="Sankey Diagram", font_size=10)
    # 显示图表
    fig.show()


# 绘制15列的桑基图 将多个桑基图数据合并为完整的时间序列，并将所有数值转换为比例
# 具体步骤：
# 读取每个CSV文件到DataFrame。
# 对每个DataFrame的value列，计算每个source的总值，用于后续的比例计算。
# 将每个value转换为占其source总值的比例。
# 将所有DataFrame合并为一个，以便绘制完整的时间序列桑基图
def convert_to_proportion_for_multi_columns_sankey():
    def convert_to_proportion(df):
        # 计算每个source的总value
        total_values_per_source = df.groupby('source')['value'].sum().reset_index()
        total_values_per_source.columns = ['source', 'total_value']
        # 将总value合并回原DataFrame
        df = pd.merge(df, total_values_per_source, on='source', how='left')
        # 计算比例
        df['proportion'] = df['value'] / df['total_value']
        # 保留必要的列
        df = df[['source', 'target', 'proportion']]
        df.rename(columns={'proportion': 'value'}, inplace=True)
        return df

    date1 = '2020_12'
    date2 = '2021_01'
    date3 = '2021_02'
    # 读取CSV文件
    df_2019_12_to_2020_01 = pd.read_csv(
        fr'G:\record\retweet_user_bias\formatted_cross_tab_result_{date1}_to_{date2}.csv')
    df_2020_01_to_2020_02 = pd.read_csv(
        fr'G:\record\retweet_user_bias\formatted_cross_tab_result_{date2}_to_{date3}.csv')
    # 转换数值为比例
    df_2019_12_to_2020_01 = convert_to_proportion(df_2019_12_to_2020_01)
    df_2020_01_to_2020_02 = convert_to_proportion(df_2020_01_to_2020_02)
    print(df_2019_12_to_2020_01)
    print(df_2020_01_to_2020_02)
    # 合并DataFrame
    df_combined = pd.concat([df_2019_12_to_2020_01, df_2020_01_to_2020_02])
    # 保存合并后的DataFrame
    df_combined.to_csv(r'G:\record\retweet_user_bias\combined_multi_columns_sankey_data_tmp.csv', index=False)
    # 显示合并后的DataFrame
    print(df_combined)


def plot_multi_columns_sankey():
    # 一个月与下一个月之间的相同用户：
    # csv_file = r'G:\record\retweet_user_bias\combined_multi_columns_sankey_data_2019_12_to_2020_05.csv'
    # csv_file = r'G:\record\retweet_user_bias\combined_multi_columns_sankey_data_2020_05_to_2020_10.csv'
    # csv_file = r'G:\record\retweet_user_bias\combined_multi_columns_sankey_data_2020_10_to_2021_02.csv'
    # csv_file = r'G:\record\retweet_user_bias\every_other_month\this_month_to_next_month_absolute_value_cross_table\new_absolute_value.xlsx'
    # 一个季度与下一个季度之间的相同用户：
    csv_file = r'G:\record\retweet_user_bias\every_three_months\this_quarter_to_next_quarter_absolute_value_cross_table\every_quarter_absolute_value.xlsx'

    df = pd.read_excel(csv_file, header=None)
    # 由于CSV格式并非标准的长格式，我们需要处理数据
    # 每三列是一个时间段的数据，总共有3个时间段，即9列
    # 我们将这些数据转换为长格式
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
    # 查看数据
    print(long_df.head())

    # 接下来，绘制桑基图：
    # 获取所有唯一的节点
    nodes = list(set(long_df['source']).union(set(long_df['target'])))

    # 节点映射到数字ID，因为Plotly的Sankey图需要用数字ID来表示节点
    node_dict = {node: i for i, node in enumerate(nodes)}
    # 更新颜色映射为更美观的RGB颜色
    node_color_map = {
        'LEFT': 'rgb(052, 073, 100)',  # 深蓝色
        'CENTER': 'rgb(240, 245, 182)',  # 亮黄色
        'RIGHT': 'rgb(210, 077, 083)',  # 深红色
        'DEFAULT': 'rgb(200, 200, 200)'  # 默认灰色
    }
    # 连边颜色映射
    link_color_map = {
        'LEFT': 'rgba(177, 217, 299, 0.5)',  # 浅蓝色，半透明
        'CENTER': 'rgba(250, 252, 228, 0.9)',  # 浅黄色，半透明
        'RIGHT': 'rgba(245, 186, 186, 0.5)',  # 浅红色，半透明
        'DEFAULT': 'rgba(200, 200, 200, 0.5)'  # 默认灰色，半透明
    }

    # 定义一个函数，用于从节点名称中提取颜色关键字
    def extract_color_suffix(node_name):
        if node_name.endswith('LEFT'):
            return 'LEFT'
        elif node_name.endswith('CENTER'):
            return 'CENTER'
        elif node_name.endswith('RIGHT'):
            return 'RIGHT'
        else:
            return 'DEFAULT'  # 对于不匹配任何关键字的节点，返回一个默认值

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


# 首先合并每3-4个月的用户id的总分、并且重新计算用户平均分
# 具体步骤：四个文件中一行行的处理过程中遇到之前处理过的相同的id就需要把对应的总分、次数加起来，处理完所有文件之后需要把四个文件的id、总分、次数保存在新的csv文件里，并且把每行数据的平均值也算出来保存在每行的第四列里（用总分除以次数得到平均值），最后把新csv文件按照第四列的值从小到大进行排序
# 生成G:\record\retweet_user_bias\every_three_months\this_quarter_to_next_quarter_common_users_average_scores\combined_retweet_user_bias_2019_12_to_2020_03.csv里的四个季度的用户id、用户出现次数、用户总分、用户平均值
def merge_user_bias_score_between_two_quarters():
    # 文件路径列表
    file_paths = [
        "G:\\record\\retweet_user_bias\\monthly_user_socres\\merge_2020_12_retweet_user_bias.csv",
        "G:\\record\\retweet_user_bias\\monthly_user_socres\\merge_2021_01_retweet_user_bias.csv",
        "G:\\record\\retweet_user_bias\\monthly_user_socres\\merge_2021_02_retweet_user_bias.csv",
        # "G:\\record\\retweet_user_bias\\monthly_user_socres\\merge_2020_11_retweet_user_bias.csv"
    ]

    # 初始化一个空的DataFrame用于合并所有数据
    combined_df = pd.DataFrame()

    # 遍历所有文件
    for path in file_paths:
        # 读取每个CSV文件
        df = pd.read_csv(path)

        # 如果combined_df为空，直接赋值，否则按'retweeted_user_id'合并，合并规则为求和
        if combined_df.empty:
            combined_df = df
        else:
            combined_df = combined_df.merge(df, on='retweeted_user_id', how='outer', suffixes=('', '_drop'))

            # 处理重复的列
            for col in df.columns[1:]:  # 除'id'外的所有列
                combined_col = col + '_drop'
                combined_df[col] = combined_df[col].fillna(0) + combined_df[combined_col].fillna(0)
                combined_df.drop(combined_col, axis=1, inplace=True)

    # 计算平均分
    combined_df['average_score'] = combined_df['bias_total_score'] / combined_df['occurrences']

    # 根据平均分排序
    combined_df = combined_df.sort_values(by='average_score')

    # 保存结果到新的CSV文件
    output_path = r"G:\record\retweet_user_bias\every_three_months\this_quarter_to_next_quarter_common_users_average_scores\combined_retweet_user_bias_2020_12_to_2021_01.csv"
    combined_df.to_csv(output_path, index=False)

    print("合并完成，文件已保存至:", output_path)


# 找到G:\record\retweet_user_bias\every_three_months\this_quarter_to_next_quarter_common_users_average_scores\combined_retweet_user_bias_2019_12_to_2020_03.csv里的四个季度的用户id、用户出现次数、用户总分、用户平均值
# 找到四个季度的csv文件里的相同用户id，生成从这个季度到下一个季度的观念分数变化文件
def find_common_user_between_two_quarters():
    # # 读取CSV文件
    date1 = '2020_08_to_2020_11'
    date2 = '2020_12_to_2021_01'
    # # 使用f-string来插入变量值
    df_2019_12 = pd.read_csv(
        fr'G:\record\retweet_user_bias\every_three_months\this_quarter_to_next_quarter_common_users_average_scores\combined_retweet_user_bias_{date1}.csv',
        usecols=['retweeted_user_id', 'average_score'])
    df_2020_01 = pd.read_csv(
        fr'G:\record\retweet_user_bias\every_three_months\this_quarter_to_next_quarter_common_users_average_scores\combined_retweet_user_bias_{date2}.csv',
        usecols=['retweeted_user_id', 'average_score'])
    # 重命名列以区分两个文件
    df_2019_12.rename(columns={'average_score': f'{date1}_average_score'}, inplace=True)
    df_2020_01.rename(columns={'average_score': f'{date2}_average_score'}, inplace=True)
    # 合并两个DataFrame，基于'retweeted_user_id'
    common_retweeted_user_id_csv_file = fr'G:\record\retweet_user_bias\every_three_months\merged_two_quarters_average_scores_{date1}-{date2}.csv'
    merged_df = pd.merge(df_2019_12, df_2020_01, on='retweeted_user_id')
    # 保存到新的CSV文件
    merged_df.to_csv(common_retweeted_user_id_csv_file, index=False)
    print('相同用户id及其观念平均值变化文件已保存在：', common_retweeted_user_id_csv_file)
    # 读取CSV文件
    df = pd.read_csv(common_retweeted_user_id_csv_file)
    # 计算每个区间的数量
    count_2019_12 = {
        '[-2, -0.5]': df[(df[f'{date1}_average_score'] >= -2) & (df[f'{date1}_average_score'] <= -0.5)].shape[0],
        '(-0.5, 0.5)': df[(df[f'{date1}_average_score'] > -0.5) & (df[f'{date1}_average_score'] < 0.5)].shape[0],
        '[0.5, 2]': df[(df[f'{date1}_average_score'] >= 0.5) & (df[f'{date1}_average_score'] <= 2)].shape[0]
    }

    count_2020_01 = {
        '[-2, -0.5]': df[(df[f'{date2}_average_score'] >= -2) & (df[f'{date2}_average_score'] <= -0.5)].shape[0],
        '(-0.5, 0.5)': df[(df[f'{date2}_average_score'] > -0.5) & (df[f'{date2}_average_score'] < 0.5)].shape[0],
        '[0.5, 2]': df[(df[f'{date2}_average_score'] >= 0.5) & (df[f'{date2}_average_score'] <= 2)].shape[0]
    }
    # 打印每个区间的数量
    print(f'{date1}的各区间数量:', count_2019_12)
    print(f'{date2}的各区间数量:', count_2020_01)
    # 定义区间计数器
    transitions = {
        f'{date1}_[-2, -0.5] to {date2}_[-2, -0.5]': 0,
        f'{date1}_[-2, -0.5] to {date2}_(-0.5, 0.5)': 0,
        f'{date1}_[-2, -0.5] to {date2}_[0.5, 2]': 0,
        f'{date1}_(-0.5, 0.5) to {date2}_[-2, -0.5]': 0,
        f'{date1}_(-0.5, 0.5) to {date2}_(-0.5, 0.5)': 0,
        f'{date1}_(-0.5, 0.5) to {date2}_[0.5, 2]': 0,
        f'{date1}_[0.5, 2] to {date2}_[-2, -0.5]': 0,
        f'{date1}_[0.5, 2] to {date2}_(-0.5, 0.5)': 0,
        f'{date1}_[0.5, 2] to {date2}_[0.5, 2]': 0
    }

    # 统计区间转变
    for index, row in df.iterrows():
        score_2019 = row[f'{date1}_average_score']
        score_2020 = row[f'{date2}_average_score']

        if -2 <= score_2019 <= -0.5:
            if -2 <= score_2020 <= -0.5:
                transitions[f'{date1}_[-2, -0.5] to {date2}_[-2, -0.5]'] += 1
            elif -0.5 < score_2020 < 0.5:
                transitions[f'{date1}_[-2, -0.5] to {date2}_(-0.5, 0.5)'] += 1
            elif 0.5 <= score_2020 <= 2:
                transitions[f'{date1}_[-2, -0.5] to {date2}_[0.5, 2]'] += 1

        elif -0.5 < score_2019 < 0.5:
            if -2 <= score_2020 <= -0.5:
                transitions[f'{date1}_(-0.5, 0.5) to {date2}_[-2, -0.5]'] += 1
            elif -0.5 < score_2020 < 0.5:
                transitions[f'{date1}_(-0.5, 0.5) to {date2}_(-0.5, 0.5)'] += 1
            elif 0.5 <= score_2020 <= 2:
                transitions[f'{date1}_(-0.5, 0.5) to {date2}_[0.5, 2]'] += 1

        elif 0.5 <= score_2019 <= 2:
            if -2 <= score_2020 <= -0.5:
                transitions[f'{date1}_[0.5, 2] to {date2}_[-2, -0.5]'] += 1
            elif -0.5 < score_2020 < 0.5:
                transitions[f'{date1}_[0.5, 2] to {date2}_(-0.5, 0.5)'] += 1
            elif 0.5 <= score_2020 <= 2:
                transitions[f'{date1}_[0.5, 2] to {date2}_[0.5, 2]'] += 1

    # 打印每个转变的数量及验证总和
    for k, v in transitions.items():
        print(f'{k}: {v}')
    # 验证转变总和是否等于原始区间数量
    print(
        f"验证：[-2, -0.5]总和 {transitions[f'{date1}_[-2, -0.5] to {date2}_[-2, -0.5]'] + transitions[f'{date1}_[-2, -0.5] to {date2}_(-0.5, 0.5)'] + transitions[f'{date1}_[-2, -0.5] to {date2}_[0.5, 2]']} 应等于 {count_2019_12['[-2, -0.5]']}")
    print(
        f"验证：(-0.5, 0.5)总和 {transitions[f'{date1}_(-0.5, 0.5) to {date2}_[-2, -0.5]'] + transitions[f'{date1}_(-0.5, 0.5) to {date2}_(-0.5, 0.5)'] + transitions[f'{date1}_(-0.5, 0.5) to {date2}_[0.5, 2]']} 应等于 {count_2019_12['(-0.5, 0.5)']}")
    print(
        f"验证：[0.5, 2]总和 {transitions[f'{date1}_[0.5, 2] to {date2}_[-2, -0.5]'] + transitions[f'{date1}_[0.5, 2] to {date2}_(-0.5, 0.5)'] + transitions[f'{date1}_[0.5, 2] to {date2}_[0.5, 2]']} 应等于 {count_2019_12['[0.5, 2]']}")


if __name__ == "__main__":
    # # 文件路径
    # user_ids_csv_path = 'G:\\record\\count_user_id_record\\origin_retweet_user\\total-count-origin-user-id.csv'
    # data_csv_paths = find_csv_paths()# 查找所有满足条件的CSV文件路径
    # output_csv_path = 'G:\\record\\count_user_id_record\\origin_retweet_user\\matched_user_names.csv'
    # # 执行函数
    # match_and_save_user_names(user_ids_csv_path, data_csv_paths, output_csv_path)

    # 匹配用户名的时候漏掉了count，补充上
    # match_count()
    # 根据用户id匹配用户的bias
    # match_political_bias()
    # 计算转帖用户的政治倾向分数总和、平均分数
    # count_monthly_retweet_user_bias()
    # 找到相同的用户id并把用户观念平均分做区间划分，最后绘制桑基图
    # find_common_user_within_two_months_and_plot_sankey()
    plot_multi_columns_sankey()
    # merge_user_bias_score_between_two_quarters()
    # find_common_user_between_two_quarters()

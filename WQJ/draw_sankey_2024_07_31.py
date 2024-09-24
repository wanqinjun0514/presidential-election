import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import norm

# 每两个月之间相同用户id的bias平均值拼接在一个csv文件里
def find_common_user_between_two_months_by_politician():
    date1s = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08', '2020_09', '2020_10', '2020_11', '2020_12', '2021_01']
    date2s = ['2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08', '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']

    for date1, date2 in zip(date1s, date2s):
        # 对应twitter_url的文件路径
        # path1 = rf'F:\us-presidential-output\politician_average_rating\twitter_url-rating\{date1}_output.csv'
        # path2 = rf'F:\us-presidential-output\politician_average_rating\twitter_url-rating\{date2}_output.csv'

        # 对应external_url的文件路径
        # path1 = rf'F:\us-presidential-output\politician_average_rating\external_url-rating\{date1}_output.csv'
        # path2 = rf'F:\us-presidential-output\politician_average_rating\external_url-rating\{date2}_output.csv'

        # 对应without_url的文件路径
        path1 = rf'F:\us-presidential-output\politician_average_rating\without_url-rating\{date1}_output.csv'
        path2 = rf'F:\us-presidential-output\politician_average_rating\without_url-rating\{date2}_output.csv'

        print('正在处理：', path1, path2)
        # 读取文件
        df1 = pd.read_csv(path1, usecols=['retweeted_user_id', 'average_bias_points'],
                          dtype={'retweeted_user_id': 'str', 'average_bias_points': 'float64'})
        df2 = pd.read_csv(path2, usecols=['retweeted_user_id', 'average_bias_points'],
                          dtype={'retweeted_user_id': 'str', 'average_bias_points': 'float64'})

        # 找到相同的 retweeted_user_id
        common_ids = set(df1['retweeted_user_id']).intersection(set(df2['retweeted_user_id']))

        # 初始化字典存储结果
        result = {'retweeted_user_id': [], 'date1_average': [], 'date2_average': []}

        # 从第一个数据集中获取 date1_average
        date1_dict = df1.set_index('retweeted_user_id')['average_bias_points'].to_dict()
        date2_dict = df2.set_index('retweeted_user_id')['average_bias_points'].to_dict()

        for user_id in common_ids:
            result['retweeted_user_id'].append(user_id)
            result['date1_average'].append(date1_dict.get(user_id, None))
            result['date2_average'].append(date2_dict.get(user_id, None))

        # 创建新的 DataFrame
        merged_df = pd.DataFrame(result)

        # 保存新的CSV文件
        # output_path = rf'F:\us-presidential-output\politician_average_rating\twitter_url-rating\every_month\common_user_bias_{date1}_to_{date2}.csv'

        # output_path = rf'F:\us-presidential-output\politician_average_rating\external_url-rating\every_month\common_user_bias_{date1}_to_{date2}.csv'

        output_path = rf'F:\us-presidential-output\politician_average_rating\without_url-rating\every_month\common_user_bias\common_user_bias_{date1}_to_{date2}.csv'


        merged_df.to_csv(output_path, index=False)


# 统计构建媒体数据对用户观念影响的桑基图的矩阵数据
# 从上一个月的七类政治倾向变化到下一个月的七类政治倾向的桑基图  矩阵数据是3*4的，保存到csv文件里
def Construct_matrix_data_for_drawing_Sankey_diagrams_by_politician():
    date1s = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
              '2020_09', '2020_10', '2020_11', '2020_12', '2021_01']
    date2s = ['2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08', '2020_09',
              '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']

    for date1, date2 in zip(date1s, date2s):
        # 载入数据1
        # file_path = rf"F:\us-presidential-output\politician_average_rating\twitter_url-rating\every_month\common_user_bias_{date1}_to_{date2}.csv"
        # 载入数据2
        # file_path = rf"F:\us-presidential-output\politician_average_rating\external_url-rating\every_month\common_user_bias\common_user_bias_{date1}_to_{date2}.csv"
        # 载入数据3
        file_path = rf"F:\us-presidential-output\politician_average_rating\without_url-rating\every_month\common_user_bias\common_user_bias_{date1}_to_{date2}.csv"
        df = pd.read_csv(file_path)
        # 定义区间和标签
        labels = ['Left', 'Center', 'Right']

        # 定义一个函数来分类政治倾向
        def categorize_bias(score):
            if -1 <= score <= -(1/3):
                return 'Left'
            elif -(1/3) < score < 1/3:
                return 'Center'
            elif 1/3 <= score <= 1:
                return 'Right'

        # 应用函数到数据列
        df['category_date1'] = df['date1_average'].apply(categorize_bias)
        df['category_date2'] = df['date2_average'].apply(categorize_bias)
        # 统计每个类别的数量
        count_2019_12 = df['category_date1'].value_counts()
        count_2020_01 = df['category_date1'].value_counts()
        # 初始化转换字典
        transitions = {f'{l1} to {l2}': 0 for l1 in labels for l2 in labels}
        # 计算类别间的转换
        for _, row in df.iterrows():
            transitions[f'{row["category_date1"]} to {row["category_date2"]}'] += 1
        # 打印每个类别的数量和转换情况
        print(date1, '的各区间数量:', count_2019_12)
        print(date2, '的各区间数量:', count_2020_01)
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
            # rf"F:\us-presidential-output\politician_average_rating\twitter_url-rating\every_month\cross_table\transitions_sankey_{date1}_to_{date2}.csv",
            # rf"F:\us-presidential-output\politician_average_rating\external_url-rating\every_month\cross_table\transitions_sankey_{date1}_to_{date2}.csv",
            rf"F:\us-presidential-output\politician_average_rating\without_url-rating\every_month\cross_table\transitions_sankey_{date1}_to_{date2}.csv",

            index=False)



def plot_monthly_sankey_by_politician():
    # 日期变量
    date1s = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
              '2020_09', '2020_10', '2020_11', '2020_12', '2021_01']
    date2s = ['2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08', '2020_09',
              '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']

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
            return 'DEFAULT'

    # 节点颜色映射
    node_color_map = {
        'Extreme bias Left': 'rgb(0, 51, 102)',
        'Left': 'rgb(51, 102, 153)',
        'Left leaning': 'rgb(181, 216, 243)',
        'Center': 'rgb(240, 230, 140)',
        'Right leaning': 'rgb(255, 153, 153)',
        'Right': 'rgb(204, 102, 102)',
        'Extreme bias right': 'rgb(139, 26, 26)',
        'DEFAULT': 'rgb(128, 128, 128)'
    }

    # 连边颜色映射
    link_color_map = {key: 'rgba' + value[3:-1] + ',0.5)' for key, value in node_color_map.items()}

    for date1, date2 in zip(date1s, date2s):
        # file_path = f'F:\\us-presidential-output\\politician_average_rating\\twitter_url-rating\\every_month\\cross_table\\transitions_sankey_{date1}_to_{date2}.csv'
        # file_path = f'F:\\us-presidential-output\\politician_average_rating\\external_url-rating\\every_month\\cross_table\\transitions_sankey_{date1}_to_{date2}.csv'
        file_path = f'F:\\us-presidential-output\\politician_average_rating\\twitter_url-rating\\every_month\\cross_table\\transitions_sankey_{date1}_to_{date2}.csv'
        df = pd.read_csv(file_path)

        nodes = set(df['source']).union(set(df['target']))
        node_dict = {node: i for i, node in enumerate(nodes)}

        # 设置节点颜色
        node_colors = [node_color_map[extract_color_suffix(node)] for node in nodes]

        # 设置连边颜色
        link_colors = [link_color_map[extract_color_suffix(source)] for source in df['source']]

        link = {
            'source': df['source'].map(node_dict),
            'target': df['target'].map(node_dict),
            'value': df['value'],
            'color': link_colors
        }

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color='black', width=0.5),
                label=list(node_dict),
                color=node_colors
            ),
            link=dict(
                source=link['source'],
                target=link['target'],
                value=link['value'],
                color=link['color']
            )
        )])
        fig.update_layout(title_text=f"Sankey Diagram from {date1} to {date2}", font_size=10)



        fig.show()
        print(f"桑基图",date1 ,' to ', date2)

# 如果这段代码是在Jupyter Notebook或其他互动环境中运行，可以直接调用此函数绘制图表。



def politician_Normal_distribution_plot_every_month():
    # 指定文件夹路径
    folder_path = 'F:\\us-presidential-output\\politician_average_rating\\twitter_url-rating'

    # 获取所有CSV文件
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # 创建文件保存目录
    output_folder = 'F:\\us-presidential-output\\politician_average_rating\\twitter_url-rating\\graphs'
    os.makedirs(output_folder, exist_ok=True)

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 提取average_bias_points列的数据
        data = df['average_bias_points']

        # 绘制正态分布图
        plt.figure(figsize=(10, 6))
        plt.hist(data, bins=30, density=True, alpha=0.6, color='g', label='Data histogram')

        # 拟合正态分布
        mu, std = norm.fit(data)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2, label=f'Normal fit ($\mu={mu:.2f}$, $\sigma={std:.2f}$)')

        plt.xlabel('Average Bias Points')
        plt.ylabel('Density')
        plt.title(f'Normal Distribution of {file}')
        plt.legend()

        # 保存图像
        output_file = os.path.join(output_folder, f'{file}_distribution.png')
        plt.savefig(output_file)
        plt.close()

    print("All graphs have been saved to the output folder.")

def politician_Normal_distribution_plot():
    # 指定文件夹路径
    folder_path = 'F:\\us-presidential-output\\politician_average_rating\\twitter_url-rating'

    # 获取所有CSV文件
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # 创建一个空列表来存储所有的average_bias_points数据
    all_data = []

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 提取average_bias_points列的数据，并添加到all_data列表
        all_data.extend(df['average_bias_points'].tolist())

    # 转换为NumPy数组以便于处理
    all_data = np.array(all_data)

    # 绘制总的正态分布图
    plt.figure(figsize=(10, 6))
    plt.hist(all_data, bins=30, density=True, alpha=0.6, color='g', label='Data histogram')

    # 拟合正态分布
    mu, std = norm.fit(all_data)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2, label=f'Normal fit ($\mu={mu:.2f}$, $\sigma={std:.2f}$)')

    plt.xlabel('Average Bias Points')
    plt.ylabel('Density')
    plt.title('Overall Normal Distribution of Average Bias Points')
    plt.legend()

    # 显示图像
    plt.show()


def draw_total_sankey():
    # 文件夹路径
    folder_path = r'F:\us-presidential-output\politician_average_rating\twitter_url-rating\every_month\cross_table'
    all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

    # 读取并合并所有文件
    data_frames = []
    for file in all_files:
        df = pd.read_csv(file)
        data_frames.append(df)
    combined_df = pd.concat(data_frames)

    # 获取所有唯一的节点
    sources = set(combined_df['source'])
    targets = set(combined_df['target'])
    nodes = list(sources.union(targets))
    node_dict = {node: i for i, node in enumerate(sorted(nodes))}

    # 定义节点颜色映射
    node_color_map = {
        'Extreme bias Left': 'rgb(0, 51, 102)',  # 最深蓝色
        'Left': 'rgb(51, 102, 153)',  # 深蓝色
        'Left leaning': 'rgb(181, 216, 243)',  # 中等蓝色
        'Center': 'rgb(240, 230, 140)',  # 浅黄色
        'Right leaning': 'rgb(255, 153, 153)',  # 浅红色
        'Right': 'rgb(204, 102, 102)',  # 中等红色
        'Extreme bias right': 'rgb(139, 26, 26)',  # 深红色
        'DEFAULT': 'rgb(128, 128, 128)'  # 默认灰色
    }

    # 为节点分配颜色
    node_colors = [node_color_map.get(node.split('_')[-1], 'rgb(128, 128, 128)') for node in nodes]

    # 为连边分配颜色，确保与源节点相同
    link_colors = [node_color_map.get(source.split('_')[-1], 'rgba(128, 128, 128, 0.5)') for source in combined_df['source']]

    # 创建桑基图的数据结构
    links = {
        'source': combined_df['source'].map(node_dict),
        'target': combined_df['target'].map(node_dict),
        'value': combined_df['value'],
        'color': link_colors
    }

    # 创建桑基图
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=sorted(nodes),
            color=node_colors  # 设置节点颜色
        ),
        link=dict(
            source=links['source'],
            target=links['target'],
            value=links['value'],
            color=links['color']  # 设置连边颜色
        )
    )])

    # 设置图表的标题
    fig.update_layout(title_text="Monthly Transition Sankey Diagram", font_size=12)

    # 显示图表
    fig.show()

if __name__ == "__main__":

    # politician_Normal_distribution_plot()
    # find_common_user_between_two_months_by_media()
    # Construct_matrix_data_for_drawing_Sankey_diagrams_by_media()
    plot_monthly_sankey_by_politician()
    # draw_total_sankey()
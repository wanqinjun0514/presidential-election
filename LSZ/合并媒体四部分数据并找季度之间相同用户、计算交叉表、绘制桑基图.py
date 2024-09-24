import pandas as pd
import os
import plotly.graph_objects as go
import re
# 帮我根据F:\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating下的所有以user_bias_scores_开头的csv做一个季度数据的统计，一共有15个月，我们分成五个季度：'2019_12_2020_01_2020_02', '2020_03_2020_04_2020_05', '2020_06_2020_07_2020_08', '2020_09_2020_10', '2020_11_2020_12'，'2021_01_2021_02'
# 就是读取external_url-rating下的user_bias_scores_2019_12、user_bias_scores_2020_01、user_bias_scores_2020_02这三个月的数据，每个csv都是以user_id,total_score,appearance_count,average_bias_points为表头，以user_id为主键，将一个季度里所有月份的相同的user_id对应的total_score和appearance_count进行累加
# 遍历完所有的csv之后，再对每个用户对应的累加好的total_score和appearance_count进行求平均值，用total_score除以appearance_count算出average_bias_points为表头列的数据
# 最后每个季度的用户保存一个文件，表头是user_id,total_score,appearance_count,average_bias_points。是累加好的total_score和appearance_count，以及更新了的average_bias_points
def process_quarterly_user_bias_scores():


    # 定义文件夹路径和每个季度包含的月份
    base_path = rf'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\user_bias_scores_by_quarter'
    quarter_months = [
        ['2019_12', '2020_01', '2020_02'],
        ['2020_03', '2020_04', '2020_05'],
        ['2020_06', '2020_07', '2020_08'],
        ['2020_09', '2020_10'],
        ['2020_11', '2020_12'],
        ['2021_01', '2021_02']
    ]

    # 遍历每个季度的月份
    for i, months in enumerate(quarter_months):
        # 初始化一个空的DataFrame来累加数据
        quarterly_data = pd.DataFrame()

        # 遍历季度中的每个月份
        for month in months:
            file_path = os.path.join(base_path, f'quarterly_user_bias_scores_{month}.csv')

            if os.path.exists(file_path):
                # 读取CSV文件
                temp_df = pd.read_csv(file_path,
                                      usecols=['user_id', 'total_score', 'appearance_count', 'average_bias_points'],
                                      dtype={'user_id': 'str', 'total_score': 'float64', 'appearance_count': 'int64'})

                # 累加相同user_id的total_score和appearance_count
                if quarterly_data.empty:
                    quarterly_data = temp_df
                else:
                    quarterly_data = pd.concat([quarterly_data, temp_df])
                    quarterly_data = quarterly_data.groupby('user_id', as_index=False).agg({
                        'total_score': 'sum',
                        'appearance_count': 'sum'
                    })

        # 计算新的average_bias_points
        quarterly_data['average_bias_points'] = quarterly_data['total_score'] / quarterly_data['appearance_count']

        # 生成季度字符串并保存文件
        quarter_str = "_".join(months)
        output_file = os.path.join(base_path, f'quarterly_user_bias_scores_{quarter_str}.csv')
        quarterly_data.to_csv(output_file, index=False)

        print(f"Saved quarterly data for {quarter_str} to {output_file}")


# 每两个季度之间相同用户id的bias平均值拼接在一个csv文件里
def find_common_users_between_quarters():

    base_path = rf'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\user_bias_scores_by_quarter'
    quarter_files = [
        'quarterly_user_bias_scores_2019_12_2020_01_2020_02.csv',
        'quarterly_user_bias_scores_2020_03_2020_04_2020_05.csv',
        'quarterly_user_bias_scores_2020_06_2020_07_2020_08.csv',
        'quarterly_user_bias_scores_2020_09_2020_10.csv',
        'quarterly_user_bias_scores_2020_11_2020_12.csv',
        'quarterly_user_bias_scores_2021_01_2021_02.csv'
    ]

    for i in range(len(quarter_files) - 1):
        path1 = os.path.join(base_path, quarter_files[i])
        path2 = os.path.join(base_path, quarter_files[i + 1])

        # 输出文件路径
        q1_str = quarter_files[i].replace('quarterly_user_bias_scores_', '').replace('.csv', '')
        q2_str = quarter_files[i + 1].replace('quarterly_user_bias_scores_', '').replace('.csv', '')
        output_path = rf'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\sankey_plot\every_quarter\common_user_bias\common_users_{q1_str}_to_{q2_str}.csv'

        # 读取两个季度的文件
        df1 = pd.read_csv(path1, usecols=['user_id', 'average_bias_points'],
                          dtype={'user_id': 'str', 'average_bias_points': 'float64'})
        df2 = pd.read_csv(path2, usecols=['user_id', 'average_bias_points'],
                          dtype={'user_id': 'str', 'average_bias_points': 'float64'})

        # 更改列名以区分
        df1.rename(columns={'average_bias_points': 'date1_average'}, inplace=True)
        df2.rename(columns={'average_bias_points': 'date2_average'}, inplace=True)

        # 查找相同用户
        common_users = pd.merge(df1[['user_id', 'date1_average']], df2[['user_id', 'date2_average']], on='user_id')

        # 输出相同用户数据
        print(f"Common users between {q1_str} and {q2_str}:")
        print(common_users)
        common_users.to_csv(output_path, index=False)

        print(f"Saved common users between {q1_str} and {q2_str} to {output_path}")



# 统计构建媒体数据对用户观念影响的桑基图的矩阵数据
# 从上一个月的七类政治倾向变化到下一个月的七类政治倾向的桑基图  矩阵数据是7*7的，保存到csv文件里
def Construct_matrix_data_for_drawing_Sankey_diagrams_by_media():
    # data_part_name = 'external_url'
    # data_part_name = 'without_url'
    # data_part_name = 'twitter_url'
    data_part_name = 'multiple_url'
    # 文件路径设置
    date1s = ['2019_12_2020_01_2020_02', '2020_03_2020_04_2020_05', '2020_06_2020_07_2020_08', '2020_09_2020_10', '2020_11_2020_12']
    date2s = ['2020_03_2020_04_2020_05', '2020_06_2020_07_2020_08', '2020_09_2020_10', '2020_11_2020_12', '2021_01_2021_02']
    for date1, date2 in zip(date1s, date2s):
        # 载入数据
        file_path = rf"F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\sankey_plot\every_quarter\common_user_bias\common_users_{date1}_to_{date2}.csv"

        output_transition_matrix_path = rf"F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\sankey_plot\every_quarter\cross_table\transitions_sankey_{date1}_to_{date2}.csv"
        os.makedirs(os.path.dirname(output_transition_matrix_path), exist_ok=True)  # 如果路径不存在 则创建新目录新文件夹，加这一句
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
        df['date1_average'] = df['date1_average'].apply(categorize_bias)
        df['date2_average'] = df['date2_average'].apply(categorize_bias)
        # 统计每个类别的数量
        count_2019_12 = df['date1_average'].value_counts()
        count_2020_01 = df['date2_average'].value_counts()
        # 初始化转换字典
        transitions = {f'{l1} to {l2}': 0 for l1 in labels for l2 in labels}
        # 计算类别间的转换
        for _, row in df.iterrows():
            transitions[f'{row["date1_average"]} to {row["date2_average"]}'] += 1
        # 打印每个类别的数量和转换情况
        print('date1的各区间数量:', count_2019_12)
        print('date2的各区间数量:', count_2020_01)
        # 计算总和并打印
        total_count_2019_12 = count_2019_12.sum()
        total_count_2020_01 = count_2020_01.sum()

        print('count_2019_12的总和:', total_count_2019_12)
        print('count_2020_01的总和:', total_count_2020_01)
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
            output_transition_matrix_path,index=False)

# 帮我统计一下F:\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating\sankey_plot\cross_table下的所有csv，所有csv的表头都是source,target,value。对每一个csv都计算出一个value列数据的总和出来
def 检查交叉表里的value数据之和是否和两个月份之间的相同用户数量相同():
    # 文件夹路径
    folder_path = r"F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\sankey_plot\every_quarter\cross_table"

    # 初始化一个字典来存储每个文件的value列总和
    file_value_sums = {}

    # 遍历文件夹下所有的csv文件
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)

            # 检查文件中是否有'value'列
            if 'value' in df.columns:
                # 计算value列的总和
                value_sum = df['value'].sum()
                # 将结果存入字典
                file_value_sums[file] = value_sum
    # 遍历file_value_sums，打印出表格形式的数据
    print("月份/数据量\t相邻月份之间相同用户数量")
    for file, value_sum in file_value_sums.items():
        # 打印每个文件名以及对应的value列总和
        print(f"{file}\t{value_sum}")



def plot_quaterly_sankey_by_meida():
    # data_part_name = 'external_url'
    # data_part_name = 'without_url'
    # data_part_name = 'twitter_url'
    data_part_name = 'multiple_url'
    # 一个月与下一个月之间的相同用户：
    # 一个季度与下一个季度之间的相同用户：
    # 文件路径设置
    date1s = ['2019_12_2020_01_2020_02', '2020_03_2020_04_2020_05', '2020_06_2020_07_2020_08', '2020_09_2020_10',
              '2020_11_2020_12']
    date2s = ['2020_03_2020_04_2020_05', '2020_06_2020_07_2020_08', '2020_09_2020_10', '2020_11_2020_12',
              '2021_01_2021_02']
    for date1, date2 in zip(date1s, date2s):
        csv_file = rf'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\sankey_plot\every_quarter\cross_table\transitions_sankey_{date1}_to_{date2}.csv'

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

# 批量重命名newplot.png
def quaterly_change_name():
    # data_part_name = 'external_url'
    # data_part_name = 'without_url'
    # data_part_name = 'twitter_url'
    data_part_name = 'multiple_url'
    # 文件夹路径
    folder_path = rf'F:\Experimental Results\Average_Bias_Rating\media_average_rating\total_url-rating\sankey_plot\every_quarter\Sankey_plot'

    # 目标文件名列表
    new_filenames = [
        "common_user_bias_2019_12_2020_01_2020_02_to_2020_03_2020_04_2020_05.png",
        "common_user_bias_2020_03_2020_04_2020_05_to_2020_06_2020_07_2020_08.png",
        "common_user_bias_2020_06_2020_07_2020_08_to_2020_09_2020_10.png",
        "common_user_bias_2020_09_2020_10_to_2020_11_2020_12.png",
        "common_user_bias_2020_11_2020_12_to_2021_01_2021_02.png",
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



if __name__ == '__main__':
    # # process_quarterly_user_bias_scores()
    # find_common_users_between_quarters()
    # Construct_matrix_data_for_drawing_Sankey_diagrams_by_media()
    # 检查交叉表里的value数据之和是否和两个月份之间的相同用户数量相同()
    # plot_quaterly_sankey_by_meida()
    quaterly_change_name()
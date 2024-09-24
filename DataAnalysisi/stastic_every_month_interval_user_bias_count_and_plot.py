import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

#对G:\record\retweet_user_bias\monthly_user_socres文件夹下所有的以_retweet_user_bias.csv结尾的文件进行分析，这些csv文件有表头分别是：retweeted_user_id,bias_total_score,occurrences,average_score，只需要读取average_score这一列的数据，
# 统计有多少average_score数据在[-2,-0.5]之间，有多少数据在[-0.5,0.5]之间，有多少数据在[0.5,2]之间，对于每一个csv都输出一下统计结果
# 仅仅做输出 不存文件
def stastic_every_month_interval_user_bias_count():
    # 文件夹路径
    directory_path = r'G:\record\retweet_user_bias\monthly_user_socres'
    # 匹配模式，找到所有以_retweet_user_bias.csv结尾的文件
    pattern = os.path.join(directory_path, '*_retweet_user_bias.csv')
    files = glob.glob(pattern)
    total_count_across_files = 0  # 跨所有文件的数据总数
    # 定义分数区间
    intervals = [[-2, -0.5], (-0.5, 0.5), [0.5, 2]]
    # 遍历所有符合条件的文件
    for file_path in files:
        # 读取CSV文件的'average_score'列
        df = pd.read_csv(file_path, usecols=['average_score'])
        # 文件名
        file_name = os.path.basename(file_path)
        interval_counts = 0  # 初始化当前文件的区间计数
        print(f'文件：{file_name} 的统计结果如下：')
        # 对每个区间进行计数
        for interval in intervals:
            if interval == intervals[0]:  # 第一个区间 [-2, -0.5]
                count = df[(df['average_score'] >= interval[0]) & (df['average_score'] <= interval[1])].shape[0]
            elif interval == intervals[1]:  # 第二个区间 (-0.5, 0.5)
                count = df[(df['average_score'] > interval[0]) & (df['average_score'] < interval[1])].shape[0]
            else:  # 第三个区间 [0.5, 2]
                count = df[(df['average_score'] >= interval[0]) & (df['average_score'] <= interval[1])].shape[0]

            interval_counts += count
            print(f'在区间 {interval} 内的average_score数量为：{count}')
        print(f'当前文件总行数：{df.shape[0]}')
        print(f'三个区间的数量总和：{interval_counts}')
        print(f'总和与文件总行数{"相等" if interval_counts == df.shape[0] else "不相等"}')
        total_count_across_files += df.shape[0]  # 更新跨所有文件的数据总数
        print('-' * 50)


#绘制一个组合柱状图，15个月份的数据作为横轴，每个月份的数据有三类：LEFT、CENTER、RIGHT
def draw_bar_chart_by_politic():
    # 给定的数据
    data = {
        'Month': [
            '2019-12', '2020-01', '2020-02', '2020-03', '2020-04',
            '2020-05', '2020-06', '2020-07', '2020-08', '2020-09',
            '2020-10', '2020-11', '2020-12', '2021-01', '2021-02'
        ],
        'LEFT': [
            434564, 468042, 487758, 848610, 645623,
            508004, 801227, 920711, 1068679, 1027090,
            1207016, 1613359, 730606, 1495229, 546233
        ],
        'CENTER': [
            14293, 12975, 12791, 26800, 18470,
            12759, 13435, 12150, 20438, 27885,
            41010, 40819, 30389, 44365, 35504
        ],
        'RIGHT': [
            387300, 520394, 360342, 569936, 563665,
            569255, 556092, 546464, 625065, 575682,
            931585, 837046, 604178, 538379, 273046
        ]
    }
    # 转换数据到DataFrame
    df = pd.DataFrame(data)

    # 设置柱状图的颜色
    colors = {
        'LEFT': (0.694, 0.850, 0.850, 0.5),  # 调整为接受的RGBA元组格式
        'CENTER': (0.980, 0.988, 0.894, 0.9),
        'RIGHT': (0.961, 0.729, 0.729, 0.5),
    }

    # 绘制组合柱状图
    fig, ax = plt.subplots(figsize=(15, 8))

    # 每个柱子的宽度
    bar_width = 0.25

    # 生成每个分类的位置
    r1 = range(len(df))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]

    # 绘制每个分类的柱状图
    ax.bar(r1, df['LEFT'], color=colors['LEFT'], width=bar_width, edgecolor='grey', label='LEFT')
    ax.bar(r2, df['CENTER'], color=colors['CENTER'], width=bar_width, edgecolor='grey', label='CENTER')
    ax.bar(r3, df['RIGHT'], color=colors['RIGHT'], width=bar_width, edgecolor='grey', label='RIGHT')

    # 添加图例
    ax.legend()

    # 设置标题和标签
    ax.set_xlabel('Month', fontweight='bold')
    ax.set_ylabel('Count', fontweight='bold')
    ax.set_title('Monthly Distribution of User Bias')
    ax.set_xticks([r + bar_width for r in range(len(df))])
    ax.set_xticklabels(df['Month'])

    # 显示图表
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 统计G:\with_url_data\without_twitter_top_200_user_id_bias\media_user_bias_score文件夹里所有以media_user_bias_开头的csv文件各个观念区间的值
def stastic_every_month_interval_user_bias_count_by_top200_media():
    # 文件夹路径
    directory_path = r'H:\with_url_data\without_twitter_top_200_user_id_bias\media_user_bias_score'
    # 匹配模式，找到所有以_retweet_user_bias.csv结尾的文件
    pattern = os.path.join(directory_path, 'media_user_bias_*.csv')
    files = glob.glob(pattern)
    total_count_across_files = 0  # 跨所有文件的数据总数

    # 定义分数区间，注意闭开区间和完全闭区间的表示
    intervals = [(-3, -2.5), (-2.5, -1.5), (-1.5, -0.5), (-0.5, 0.5), (0.5, 1.5), (1.5, 2.5), (2.5, 3)]

    # 遍历所有符合条件的文件
    for file_path in files:
        # 读取CSV文件的'average_score'列
        df = pd.read_csv(file_path, usecols=['average'])
        # 文件名
        file_name = os.path.basename(file_path)
        interval_counts = 0  # 初始化当前文件的区间计数
        print(f'文件：{file_name} 的统计结果如下：')

        # 对每个区间进行计数
        for interval in intervals:
            if interval[1] == 3:  # 对最后一个区间使用闭区间
                count = df[(df['average'] >= interval[0]) & (df['average'] <= interval[1])].shape[0]
            else:  # 对其他区间使用左闭右开
                count = df[(df['average'] >= interval[0]) & (df['average'] < interval[1])].shape[0]

            interval_counts += count
            print(f'在区间 {interval} 内的average_score数量为：{count}')

        print(f'当前文件总行数：{df.shape[0]}')
        print(f'各区间的数量总和：{interval_counts}')
        print(f'总和与文件总行数{"相等" if interval_counts == df.shape[0] else "不相等"}')
        total_count_across_files += df.shape[0]  # 更新跨所有文件的数据总数
        print('-' * 50)

def draw_bar_chart_by_media():
    # 给定的数据
    data = {
        'Month': [
            '2019-12', '2020-01', '2020-02', '2020-03', '2020-04',
            '2020-05', '2020-06', '2020-07', '2020-08', '2020-09',
            '2020-10', '2020-11', '2020-12', '2021-01', '2021-02'
        ],
        'Extreme bias Left': [
            0, 0, 0, 0, 0,
            0, 0, 0, 0, 0,
            0, 0, 0, 0, 0
        ],
        'Left': [
            17014, 15170, 21980, 25963, 27163,
            20755, 27344, 36067, 43224, 48384,
            61478, 61868, 32648, 48704, 37340
        ],
        'Left leaning': [
            120210, 123127, 149733, 198126, 161998,
            153438, 179072, 218645, 283404, 431546,
            563310, 551155, 417320, 656382, 407744
        ],
        'Center': [
            71621, 76255, 76372, 77081, 69741,
            63423, 90204, 96353, 136549, 180305,
            253806, 414383, 259071, 375801, 296410
        ],
        'Right leaning': [
            84064, 79111, 124341, 90499, 83294,
            64886, 74844, 93520, 135350, 166551,
            231577, 266582, 192522, 253756, 197438
        ],
        'Right': [
            18517, 16798, 17288, 17326, 30217,
            27831, 34268, 30617, 32197, 66357,
            95498, 121292, 51012, 75112, 63642
        ],
        'Extreme bias right': [
            13935, 15407, 12082, 16163, 21621,
            13183, 26994, 24753, 34027, 67905,
            74965, 120769, 50460, 112405, 87726
        ]

    }
    # 转换数据到DataFrame
    df = pd.DataFrame(data)

    # 设置柱状图的颜色
    colors = {
        'Extreme bias Left':(0.694, 0.850, 0.850),
        'Left': (0.694, 0.850, 0.850, 0.8),  # 调整为接受的RGBA元组格式
        'Left leaning': (0.694, 0.850, 0.850, 0.5),
        'Center': (0.980, 0.988, 0.894, 0.9),
        'Right leaning':(0.961, 0.729, 0.729, 0.2),
        'RIGHT': (0.961, 0.729, 0.729, 0.5),
        'Extreme bias right':(0.961, 0.729, 0.729),
    }

    # 绘制组合柱状图
    fig, ax = plt.subplots(figsize=(15, 8))

    # 每个柱子的宽度
    bar_width = 0.1

    # 生成每个分类的位置
    r1 = range(len(df))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]
    r5 = [x + bar_width for x in r4]
    r6 = [x + bar_width for x in r5]
    r7 = [x + bar_width for x in r6]

    # 定义颜色字典，这里需要确保颜色字典有足够的颜色值
    colors = {
        'Extreme bias Left': 'black',  # 示例颜色
        'Left': 'blue',
        'Left leaning': 'lightblue',
        'Center': 'green',
        'Right leaning': 'pink',
        'Right': 'red',
        'Extreme bias right': 'darkred'
    }

    # 绘制每个分类的柱状图
    ax.bar(r1, df['Extreme bias Left'], color=colors['Extreme bias Left'], width=bar_width, edgecolor='grey',
           label='Extreme bias Left')
    ax.bar(r2, df['Left'], color=colors['Left'], width=bar_width, edgecolor='grey', label='Left')
    ax.bar(r3, df['Left leaning'], color=colors['Left leaning'], width=bar_width, edgecolor='grey',
           label='Left leaning')
    ax.bar(r4, df['Center'], color=colors['Center'], width=bar_width, edgecolor='grey', label='Center')
    ax.bar(r5, df['Right leaning'], color=colors['Right leaning'], width=bar_width, edgecolor='grey',
           label='Right leaning')
    ax.bar(r6, df['Right'], color=colors['Right'], width=bar_width, edgecolor='grey', label='Right')
    ax.bar(r7, df['Extreme bias right'], color=colors['Extreme bias right'], width=bar_width, edgecolor='grey',
           label='Extreme bias right')

    # 添加图例
    ax.legend()

    # 设置标题和标签
    ax.set_xlabel('Month', fontweight='bold')
    ax.set_ylabel('Count', fontweight='bold')
    ax.set_title('Monthly Distribution of User Bias')
    ax.set_xticks([r + bar_width for r in range(len(df))])
    ax.set_xticklabels(df['Month'])

    # 显示图表
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    # stastic_every_month_interval_user_bias_count()
    # draw_bar_chart()
    stastic_every_month_interval_user_bias_count_by_top200_media()
    # draw_bar_chart_by_media()







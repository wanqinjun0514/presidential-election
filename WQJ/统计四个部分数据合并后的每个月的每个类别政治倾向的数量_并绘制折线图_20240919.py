import pandas as pd
import matplotlib.pyplot as plt

def 统计政客平均值打分里所有月份里的各类政治倾向用户的数量():
    # data_part = 'without_url'
    # data_part = 'twitter_url'
    data_part = 'external_url'


    months = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
              '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']
    # 定义一个DataFrame用于保存每个月的统计结果
    result_df = pd.DataFrame(columns=['month', 'Left', 'Center', 'Right'])

    # 定义一个函数，根据average_bias_points的值进行分类
    def categorize_bias(score):
        if -1 <= score <= -(1 / 3):
            return 'Left'
        elif -(1 / 3) < score < (1 / 3):
            return 'Center'
        elif (1 / 3) <= score <= 1:
            return 'Right'

    # 循环处理每个月的数据
    for month in months:
        # 读取合并后的CSV文件
        df = pd.read_csv(
            rf'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\{data_part}-rating\monthly_users_bias\{month}_output.csv',
            encoding='utf-8')

        # 创建一个新的列，用于存储分类结果
        df['category'] = df['average_bias_points'].apply(categorize_bias)

        # 统计每个类别的数量
        category_counts = df['category'].value_counts()

        # 创建一个字典来存储统计结果
        counts = {
            'month': month,
            'Left': category_counts.get('Left', 0),
            'Center': category_counts.get('Center', 0),
            'Right': category_counts.get('Right', 0),
        }

        # 将每个月的统计结果添加到结果DataFrame中
        result_df = result_df._append(counts, ignore_index=True)

    # 将结果保存到CSV文件
    result_df.to_csv(
        rf'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\{data_part}-rating\monthly_bias_category_counts_by_month.csv',
        index=False, encoding='utf-8')

    print("分类统计完成并已保存到新的CSV文件中。")

def 政客平均值打分绘制折线图():
    # 读取CSV文件
    # data_part = 'without_url'
    # data_part = 'twitter_url'
    data_part = 'external_url'
    file_path = rf'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\{data_part}-rating\monthly_bias_category_counts_by_month.csv'
    data = pd.read_csv(file_path)

    # 设置图形大小
    plt.figure(figsize=(10, 6))

    # 绘制折线图，每个类别一条线
    # 绘制折线图，每个类别一条线，颜色及透明度根据你的要求设置
    plt.plot(data['month'], data['Left'], label='Left', color=(51 / 255, 102 / 255, 153 / 255), alpha=0.5, marker='o')
    plt.plot(data['month'], data['Center'], label='Center', color=(240 / 255, 230 / 255, 140 / 255), alpha=0.7,
             marker='o')
    plt.plot(data['month'], data['Right'], label='Right', color=(204 / 255, 102 / 255, 102 / 255), alpha=0.5,
             marker='o')

    # 添加标题和标签
    plt.title(f'{data_part} User Counts by Bias Category Over Time')
    plt.xlabel('Month')
    plt.ylabel('User Count')

    # 显示图例
    plt.legend()

    # 显示图形
    plt.xticks(rotation=45)  # 使横坐标月份倾斜显示，避免重叠
    plt.ticklabel_format(style='plain', axis='y') # plt.ticklabel_format() 方法来关闭科学计数法的显示
    plt.tight_layout()  # 调整布局
    # 保存绘图
    plt.savefig(
        rf'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\{data_part}-rating\{data_part}-user_bias_counts_plot.png')

    plt.show()

def 政客平均值打分绘制比例堆叠柱状图():
    # 读取CSV文件
    # data_part = 'without_url'
    # data_part = 'twitter_url'
    data_part = 'external_url'

    # 读取CSV文件
    file_path = rf'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\政客平均值打分的折线图汇总\比例版本\{data_part}_every_bias_proportion.csv'
    data = pd.read_csv(file_path)

    # 定义月份
    months = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
              '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']

    # 绘制堆叠柱状图
    categories = ['Extreme bias Left', 'Left', 'Left leaning', 'Center', 'Right leaning', 'Right', 'Extreme bias Right']

    # 设置图形大小
    plt.figure(figsize=(12, 6))

    # 定义颜色
    colors = {
        'Left': (51 / 255, 102 / 255, 153 / 255),
        'Center': (240 / 255, 230 / 255, 140 / 255),
        'Right': (204 / 255, 102 / 255, 102 / 255),
    }

    # 设置图形大小
    plt.figure(figsize=(12, 6))

    # 堆叠绘制
    bottom = [0] * len(months)  # 初始化底部
    for category in colors:
        plt.bar(months, data[category], label=category, bottom=bottom, color=colors[category], alpha=0.7)
        bottom = [i + j for i, j in zip(bottom, data[category])]  # 更新底部

    # 添加标题和标签
    plt.title(f'{data_part} Stacked Proportion of User Bias Categories Over Time')
    plt.xlabel('Month')
    plt.ylabel('Proportion')

    # 显示图例
    plt.legend(loc='upper right')

    # 调整x轴标签旋转
    plt.xticks(rotation=45)

    # 调整布局
    plt.tight_layout()
    # 保存绘图
    plt.savefig(
        rf'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\政客平均值打分的折线图汇总\比例版本\{data_part}-user_bias_Stacked_Proportion_Plot.png')

    # 显示图形
    plt.show()




# 对每个月份的平均分数做分类，分类函数等会在categorize_bias里提供给你，分类完之后要统计出每个季度每种分类的个数有多少个
def 统计媒体平均值打分里所有月份里的各类政治倾向用户的数量():
    # data_part = 'external_url'
    # data_part = 'multiple_url'
    # data_part = 'twitter_url'
    data_part = 'without_url'


    months = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
              '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']
    # 定义一个DataFrame用于保存每个月的统计结果
    result_df = pd.DataFrame(columns=['month', 'Extreme bias Left', 'Left', 'Left leaning', 'Center',
                                      'Right leaning', 'Right', 'Extreme bias Right', 'Unknown'])

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
    # 循环处理每个月的数据
    for month in months:
        # 读取合并后的CSV文件
        df = pd.read_csv(
            rf'F:\Experimental Results\Average_Bias_Rating\media_average_rating\{data_part}-rating\user_bias_scores_by_month\user_bias_scores_{month}.csv',
            encoding='utf-8')

        # 创建一个新的列，用于存储分类结果
        df['category'] = df['average_bias_points'].apply(categorize_bias)

        # 统计每个类别的数量
        category_counts = df['category'].value_counts()

        # 创建一个字典来存储统计结果
        counts = {
            'month': month,
            'Extreme bias Left': category_counts.get('Extreme bias Left', 0),
            'Left': category_counts.get('Left', 0),
            'Left leaning': category_counts.get('Left leaning', 0),
            'Center': category_counts.get('Center', 0),
            'Right leaning': category_counts.get('Right leaning', 0),
            'Right': category_counts.get('Right', 0),
            'Extreme bias Right': category_counts.get('Extreme bias Right', 0),
            'Unknown': category_counts.get('Unknown', 0)
        }

        # 将每个月的统计结果添加到结果DataFrame中
        result_df = result_df._append(counts, ignore_index=True)

    # 将结果保存到CSV文件
    result_df.to_csv(
        rf'F:\Experimental Results\Average_Bias_Rating\media_average_rating\{data_part}-rating\monthly_bias_category_counts_by_month.csv',
        index=False, encoding='utf-8')

    print("分类统计完成并已保存到新的CSV文件中。")

#  读取文件F:\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating\monthly_bias_category_counts_by_month.csv，表头是：month,Extreme bias Left,Left,Left leaning,Center,Right leaning,Right,Extreme bias Right，表头的含义是：月份以及各个月份的用户类别，现在需要读取这个文件绘制出一个折线图 ，图的横轴是月份，纵轴是用户数量，折线图里有七条不同颜色的线条，代表着七个不同的类别，帮我写出画图的python代码
def 媒体平均值打分绘制折线图_不带左倾版():
    # 读取CSV文件
    # data_part = 'external_url'
    # data_part = 'multiple_url'
    # data_part = 'twitter_url'
    # data_part = 'without_url'
    data_part = 'total_url'



    file_path = rf'F:\Experimental Results\Average_Bias_Rating\media_average_rating\{data_part}-rating\monthly_bias_category_counts_by_month.csv'
    data = pd.read_csv(file_path)

    # 设置图形大小
    plt.figure(figsize=(10, 6))

    # 绘制折线图，每个类别一条线
    # 绘制折线图，每个类别一条线，颜色及透明度根据你的要求设置，因为left leaning的太多了把其他数据都压缩在下面了，我把左倾的先删掉了
    plt.plot(data['month'], data['Extreme bias Left'], label='Extreme bias Left', color=(0 / 255, 51 / 255, 102 / 255),
             alpha=0.5, marker='o')
    plt.plot(data['month'], data['Left'], label='Left', color=(51 / 255, 102 / 255, 153 / 255), alpha=0.5, marker='o')
    # plt.plot(data['month'], data['Left leaning'], label='Left leaning', color=(181 / 255, 216 / 255, 243 / 255),
    #          alpha=0.5, marker='o')
    plt.plot(data['month'], data['Center'], label='Center', color=(240 / 255, 230 / 255, 140 / 255), alpha=0.7,
             marker='o')
    plt.plot(data['month'], data['Right leaning'], label='Right leaning', color=(255 / 255, 153 / 255, 153 / 255),
             alpha=0.5, marker='o')
    plt.plot(data['month'], data['Right'], label='Right', color=(204 / 255, 102 / 255, 102 / 255), alpha=0.5,
             marker='o')
    plt.plot(data['month'], data['Extreme bias Right'], label='Extreme bias Right',
             color=(139 / 255, 26 / 255, 26 / 255), alpha=0.5, marker='o')

    # 添加标题和标签
    plt.title(f'{data_part} User Counts by Bias Category Over Time (without left leaning)')
    plt.xlabel('Month')
    plt.ylabel('User Count')

    # 显示图例
    plt.legend()

    # 显示图形
    plt.xticks(rotation=45)  # 使横坐标月份倾斜显示，避免重叠
    plt.tight_layout()  # 调整布局
    # 保存绘图
    plt.savefig(
        rf'F:\Experimental Results\Average_Bias_Rating\media_average_rating\{data_part}-rating\{data_part}-user_bias_counts_plot_不带左倾版.png')

    plt.show()

def 媒体平均值打分绘制折线图():
    # 读取CSV文件
    # data_part = 'external_url'
    # data_part = 'multiple_url'
    # data_part = 'twitter_url'
    # data_part = 'without_url'
    data_part = 'total_url'



    file_path = rf'F:\Experimental Results\Average_Bias_Rating\media_average_rating\{data_part}-rating\monthly_bias_category_counts_by_month.csv'
    data = pd.read_csv(file_path)

    # 设置图形大小
    plt.figure(figsize=(10, 6))

    # 绘制折线图，每个类别一条线
    # 绘制折线图，每个类别一条线，颜色及透明度根据你的要求设置
    plt.plot(data['month'], data['Extreme bias Left'], label='Extreme bias Left', color=(0 / 255, 51 / 255, 102 / 255),
             alpha=0.5, marker='o')
    plt.plot(data['month'], data['Left'], label='Left', color=(51 / 255, 102 / 255, 153 / 255), alpha=0.5, marker='o')
    plt.plot(data['month'], data['Left leaning'], label='Left leaning', color=(181 / 255, 216 / 255, 243 / 255),
             alpha=0.5, marker='o')
    plt.plot(data['month'], data['Center'], label='Center', color=(240 / 255, 230 / 255, 140 / 255), alpha=0.7,
             marker='o')
    plt.plot(data['month'], data['Right leaning'], label='Right leaning', color=(255 / 255, 153 / 255, 153 / 255),
             alpha=0.5, marker='o')
    plt.plot(data['month'], data['Right'], label='Right', color=(204 / 255, 102 / 255, 102 / 255), alpha=0.5,
             marker='o')
    plt.plot(data['month'], data['Extreme bias Right'], label='Extreme bias Right',
             color=(139 / 255, 26 / 255, 26 / 255), alpha=0.5, marker='o')

    # 添加标题和标签
    plt.title(f'{data_part} User Counts by Bias Category Over Time')
    plt.xlabel('Month')
    plt.ylabel('User Count')

    # 显示图例
    plt.legend()

    # 显示图形
    plt.xticks(rotation=45)  # 使横坐标月份倾斜显示，避免重叠
    plt.tight_layout()  # 调整布局
    # 保存绘图
    plt.savefig(
        rf'F:\Experimental Results\Average_Bias_Rating\media_average_rating\{data_part}-rating\{data_part}-user_bias_counts_plot.png')

    plt.show()

def 媒体平均值打分绘制比例堆叠柱状图():
    # 读取CSV文件
    # data_part = 'external_url'
    # data_part = 'multiple_url'
    # data_part = 'twitter_url'
    # data_part = 'without_url'
    data_part = 'total_url'
    # 读取CSV文件
    file_path = rf'F:\Experimental Results\Average_Bias_Rating\media_average_rating\媒体平均值打分的折线图汇总\比例版本\{data_part}_every_bias_proportion.csv'
    data = pd.read_csv(file_path)

    # 定义月份
    months = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08',
              '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']

    # 绘制堆叠柱状图
    categories = ['Extreme bias Left', 'Left', 'Left leaning', 'Center', 'Right leaning', 'Right', 'Extreme bias Right']

    # 设置图形大小
    plt.figure(figsize=(12, 6))

    # 定义颜色
    colors = {
        'Extreme bias Left': (0 / 255, 51 / 255, 102 / 255),
        'Left': (51 / 255, 102 / 255, 153 / 255),
        'Left leaning': (181 / 255, 216 / 255, 243 / 255),
        'Center': (240 / 255, 230 / 255, 140 / 255),
        'Right leaning': (255 / 255, 153 / 255, 153 / 255),
        'Right': (204 / 255, 102 / 255, 102 / 255),
        'Extreme bias Right': (139 / 255, 26 / 255, 26 / 255)
    }

    # 设置图形大小
    plt.figure(figsize=(12, 6))

    # 堆叠绘制
    bottom = [0] * len(months)  # 初始化底部
    for category in colors:
        plt.bar(months, data[category], label=category, bottom=bottom, color=colors[category], alpha=0.7)
        bottom = [i + j for i, j in zip(bottom, data[category])]  # 更新底部

    # 添加标题和标签
    plt.title(f'{data_part} Stacked Proportion of User Bias Categories Over Time')
    plt.xlabel('Month')
    plt.ylabel('Proportion')

    # 显示图例
    plt.legend(loc='upper right')

    # 调整x轴标签旋转
    plt.xticks(rotation=45)

    # 调整布局
    plt.tight_layout()
    # 保存绘图
    plt.savefig(
        rf'F:\Experimental Results\Average_Bias_Rating\media_average_rating\媒体平均值打分的折线图汇总\比例版本\{data_part}-user_bias_Stacked_Proportion_Plot.png')

    # 显示图形
    plt.show()






if __name__ == '__main__':
    # 统计政客平均值打分里所有月份里的各类政治倾向用户的数量()
    # 政客平均值打分绘制折线图()
    政客平均值打分绘制比例堆叠柱状图()


    # 媒体平均值打分绘制折线图_不带左倾版()
    # 媒体平均值打分绘制折线图()

    # 媒体平均值打分绘制比例堆叠柱状图()

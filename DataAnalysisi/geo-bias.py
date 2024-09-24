import glob
import os
import numpy as np
import pandas as pd
import spacy
from langdetect import detect, LangDetectException
import langid
from opencc import OpenCC
import json
import ast
import geopandas as gpd
from shapely.geometry import Point
import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from tqdm import tqdm
import scipy.stats as stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpld3
import plotly.graph_objects as go

def select_id_in_state():

    for i in range(1, 3):
        print(i)
        # 第一个CSV文件的路径
        main_csv_path = f'H:\\with_url_data\\without_twitter_top_884_user_id_bias\\media_user_bias_score\\media_user_bias_2021_0{i}.csv'

        # 存放各州CSV文件的文件夹路径
        states_folder_path = 'H:\\state\\geo-final-result\\state'

        # 读取第一个CSV文件
        main_df = pd.read_csv(main_csv_path, dtype=str, header=0)

        # 输出文件夹路径
        output_folder_path = f'H:\\geo-bias\\2021-0{i}'

        # 如果输出文件夹不存在，则创建
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        # 遍历各州的CSV文件
        for filename in os.listdir(states_folder_path):
            if filename.endswith('.csv'):
                # print(filename)
                state_csv_path = os.path.join(states_folder_path, filename)
                state_df = pd.read_csv(state_csv_path, dtype=str, header=0)

                # 筛选存在于第一个CSV文件中的retweeted_user_id
                merged_df = state_df.merge(main_df[['retweeted_user_id', 'average']], on='retweeted_user_id', how='inner')

                # 保存到新的CSV文件
                output_csv_path = os.path.join(output_folder_path, f'{filename}')
                merged_df[['retweeted_user_id', 'average']].to_csv(output_csv_path, index=False)

        # print("所有州的筛选数据已保存。")


def statistics_15_mouth():
    # 定义文件夹路径列表
    folders = [f'H:\\geo-bias\\every_mouth\\{year}-{month:02d}' for year in range(2019, 2022) for month in range(1, 13) if
               not (year == 2019 and month < 12) and not (year == 2021 and month > 2)]
    #
    # print(folders[0])

    # 存放各州统计结果的文件夹路径
    output_folder_path = 'H:\\geo-bias\\summary'

    # 如果输出文件夹不存在，则创建
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # 遍历所有文件夹
    for state_filename in os.listdir(folders[0]):
        if state_filename.endswith('.csv'):
            state_name = os.path.splitext(state_filename)[0]
            all_state_data = []
            # print(state_name)

            # 遍历每个文件夹
            for folder in folders:
                state_csv_path = os.path.join(folder, state_filename)
                if os.path.exists(state_csv_path):
                    state_df = pd.read_csv(state_csv_path, dtype=str, header=0)
                    all_state_data.append(state_df)

            if all_state_data:
                combined_df = pd.concat(all_state_data)
                combined_df['average'] = combined_df['average'].astype(float)

                # 统计相同retweeted_user_id的出现次数，并计算average的平均值
                summary_df = combined_df.groupby('retweeted_user_id').agg(
                    count=('retweeted_user_id', 'size'),
                    average=('average', 'mean')
                ).reset_index()

                # 保存统计结果到新的CSV文件
                output_csv_path = os.path.join(output_folder_path, f'{state_name}.csv')
                summary_df.to_csv(output_csv_path, index=False)


    print("所有州的统计数据已保存。")





def output():
    # 定义文件夹路径列表
    folders = [f'H:\\geo-bias\\every_mouth\\{year}-{month:02d}' for year in range(2019, 2022) for month in range(1, 13) if
               not (year == 2019 and month < 12) and not (year == 2021 and month > 2)]

    # 指定的retweeted_user_id和州名
    specified_id = '1003801980219904000'
    specified_state = 'Alabama'  # 例如 'California'

    # 初始化一个列表，用于存储筛选出的行
    filtered_data = []

    # 遍历每个文件夹
    for folder in folders:
        # 提取文件夹名中的年份和月份
        year_month = os.path.basename(folder)

        state_csv_path = os.path.join(folder, f'{specified_state}.csv')
        if os.path.exists(state_csv_path):
            state_df = pd.read_csv(state_csv_path, dtype=str, header=0)

            # 筛选出包含指定retweeted_user_id的行
            filtered_rows = state_df[state_df['retweeted_user_id'] == specified_id]

            # 添加月份信息
            if not filtered_rows.empty:
                filtered_rows['month'] = year_month
                filtered_data.append(filtered_rows)

    print(filtered_data)

    result_df = pd.concat(filtered_data)
    print(result_df)
    # # 如果有筛选出的数据，合并并保存到新的CSV文件
    # if filtered_data:
    #     result_df = pd.concat(filtered_data)
    #
    #     # 保存结果到新的CSV文件
    #     output_csv_path = os.path.join('H:\\geo-bias\\summary', f'{specified_state}_{specified_id}.csv')
    #     result_df.to_csv(output_csv_path, index=False)
    #     print(f'筛选出的数据已保存到 {output_csv_path}')
    # else:
    #     print(f'未找到指定ID {specified_id} 在指定州 {specified_state} 的数据。')

def summary_average():
    # 包含多个CSV文件的文件夹路径
    folders = [f'H:\\geo-bias\\every_mouth\\{year}-{month:02d}' for year in range(2019, 2022) for month in range(1, 13)
               if
               not (year == 2019 and month < 12) and not (year == 2021 and month > 2)]

    for input_folder_path in folders:

        year_month = os.path.basename(input_folder_path)

        # 初始化一个列表，用于存储州名和对应的average平均值
        results = []

        # 遍历文件夹中的每个CSV文件
        for filename in os.listdir(input_folder_path):
            if filename.endswith('.csv'):
                state_name = os.path.splitext(filename)[0]  # 获取州名（去掉扩展名）
                csv_path = os.path.join(input_folder_path, filename)

                # 读取CSV文件
                df = pd.read_csv(csv_path, dtype={'retweeted_user_id': str, 'count': int, 'average': float})

                # 计算average列的平均值
                average_mean = df['average'].mean()

                # 将州名和平均值添加到结果列表中
                results.append({'state': state_name, 'average_mean': average_mean})

        # 将结果保存到新的CSV文件中
        output_df = pd.DataFrame(results)
        output_csv_path = os.path.join('H:\\geo-bias\\every_mouth_means', f'{year_month}.csv')
        output_df.to_csv(output_csv_path, index=False)

        print(f'所有州的average平均值已保存到 {output_csv_path}')


def every_mouth_change():
    # 定义文件夹路径，包含保存每个月结果的文件夹路径
    results_folder_path = 'H:\\geo-bias\\every_mouth_means'

    # 获取所有结果文件的路径
    result_files = [os.path.join(results_folder_path, f) for f in os.listdir(results_folder_path) if f.endswith('.csv')]

    # 初始化一个空的 DataFrame 用于存储最终结果
    final_df = pd.DataFrame()

    # 遍历每个结果文件，读取并添加到最终的 DataFrame 中
    for file in result_files:
        # 提取月份信息
        month = os.path.splitext(os.path.basename(file))[0].split('_')[-1]

        # 读取结果文件
        df = pd.read_csv(file)

        # 设置州名为索引
        df.set_index('state', inplace=True)

        # 重命名 'average_mean' 列为当前月份
        df.rename(columns={'average_mean': month}, inplace=True)

        # 将当前月份的数据合并到最终的 DataFrame 中
        if final_df.empty:
            final_df = df
        else:
            final_df = final_df.join(df, how='outer')

    print(final_df)

    # # 将最终结果保存到一个新的 CSV 文件中
    # output_csv_path = os.path.join(results_folder_path, 'final_average_means.csv')
    # final_df.to_csv(output_csv_path)

    # 将最终结果保存到一个新的 Excel 文件中
    output_excel_path = os.path.join(results_folder_path, 'final_average_means.xlsx')
    with pd.ExcelWriter(output_excel_path) as writer:
        final_df.to_excel(writer, sheet_name='Average Means')

    # print(f'所有州的平均值数据已保存到 {output_csv_path}')

def Two_dimensional_normal():
    input_path = 'H:\\geo-bias\\summary'
    output_path = 'H:\\geo-bias\\2-dim-normal\\summary'

    # 遍历指定目录下的所有CSV文件
    for file in glob.glob(os.path.join(input_path, '*.csv')):
        state = os.path.basename(file).split('.')[0]  # 从文件名中提取州名
        print(state)

        df = pd.read_csv(f'H:\\geo-bias\\summary\\{state}.csv', dtype={'state': str, 'count': int, 'average': float}, header=0)

        print(df.shape[0])

        # 定义区间
        bins = [-3, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3]
        labels = ['[-3, -2.5)', '[-2.5, -1.5)', '[-1.5, -0.5)', '[-0.5, 0.5)', '[0.5, 1.5)', '[1.5, 2.5)', '[2.5, 3]']

        # 将average列按照区间进行划分
        df['interval'] = pd.cut(df['average'], bins=bins, labels=labels, right=False)
        df.loc[df['average'] == 3, 'interval'] = '[2.5, 3]'

        print(df)

        # 计算每个区间的个数和比例
        interval_counts = df['interval'].value_counts().sort_index()
        interval_proportions = df['interval'].value_counts(normalize=True).sort_index()

        # 输出每个区间的个数和比例
        for interval in interval_counts.index:
            print(f"区间 {interval}: 个数 = {interval_counts[interval]}, 比例 = {interval_proportions[interval]:.4f}")

        print(interval_counts)
        print(interval_proportions)

        # 输出df中的average平均值
        df_average = df['average'].mean()
        print(f"数据集中average的平均值: {df_average:.4f}")

        # Calculate mean and standard deviation
        mean = df['average'].mean()
        std_dev = df['average'].std()

        # Generate a normal distribution based on the mean and standard deviation
        x = np.linspace(-3, 3, df.shape[0])
        y = stats.norm.pdf(x, mean, std_dev)

        # Plot the normal distribution and the data points
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, label='Normal Distribution', color='blue')
        plt.hist(df['average'], bins=60, density=True, alpha=0.6, color='g', label='Data Histogram')
        plt.xlabel('Average')
        plt.ylabel('Density')
        plt.title(f'{state}')
        plt.legend()
        plt.grid(True)
        # plt.show()

        # 保存图像到指定文件夹
        output_file = os.path.join(output_path, f'{state}_normal_distribution.png')
        plt.savefig(output_file)
        plt.close()
        print(f"{state}的图像已保存到 {output_file}")


def Two_dimensional_normal3():
    input_base_path = 'H:\\geo-bias\\every_mouth'
    output_base_path = 'H:\\geo-bias\\2-dim-normal\\every_state'

    # 创建输出目录如果不存在
    if not os.path.exists(output_base_path):
        os.makedirs(output_base_path)

    # 定义月份列表
    months = [
        '2019-12', '2020-01', '2020-02', '2020-03', '2020-04',
        '2020-05', '2020-06', '2020-07', '2020-08', '2020-09',
        '2020-10', '2020-11', '2020-12', '2021-01', '2021-02'
    ]

    # 定义区间和标签
    bins = [-3, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3]
    labels = ['[-3, -2.5)', '[-2.5, -1.5)', '[-1.5, -0.5)', '[-0.5, 0.5)', '[0.5, 1.5)', '[1.5, 2.5)', '[2.5, 3]']

    for month in months:
        input_path = os.path.join(input_base_path, month)

        # 遍历指定目录下的所有CSV文件
        for file in glob.glob(os.path.join(input_path, '*.csv')):
            state = os.path.basename(file).split('.')[0]  # 从文件名中提取州名
            state_output_path = os.path.join(output_base_path, state)

            # 创建每个州的输出目录如果不存在
            if not os.path.exists(state_output_path):
                os.makedirs(state_output_path)

            # 读取CSV文件
            df = pd.read_csv(file, dtype={'state': str, 'count': int, 'average': float}, header=0)
            print(f"数据集的总行数 ({month} - {state}): {df.shape[0]}")

            # 将average列按照区间进行划分
            df['interval'] = pd.cut(df['average'], bins=bins, labels=labels, right=False)
            df.loc[df['average'] == 3, 'interval'] = '[2.5, 3]'

            # 计算每个区间的个数和比例
            interval_counts = df['interval'].value_counts().sort_index()
            interval_proportions = df['interval'].value_counts(normalize=True).sort_index()

            # 输出每个区间的个数和比例
            for interval in interval_counts.index:
                print(
                    f"区间 {interval}: 个数 = {interval_counts[interval]}, 比例 = {interval_proportions[interval]:.4f}")

            # 输出数据集中average的平均值
            df_average = df['average'].mean()
            print(f"数据集中average的平均值 ({month} - {state}): {df_average:.4f}")

            # 计算平均值和标准差
            mean = df['average'].mean()
            std_dev = df['average'].std()

            # 根据平均值和标准差生成正态分布
            x = np.linspace(-3, 3, df.shape[0])
            y = stats.norm.pdf(x, mean, std_dev)

            # Plot the normal distribution and the data points
            plt.figure(figsize=(10, 6))
            plt.plot(x, y, label='Normal Distribution', color='blue')
            plt.hist(df['average'], bins=60, density=True, alpha=0.6, color='g', label='Data Histogram')
            plt.xlabel('Average')
            plt.ylabel('Density')
            plt.title(f'{month} - {state}')
            plt.legend()
            plt.grid(True)

            # 保存图像到指定文件夹
            output_file = os.path.join(state_output_path, f'{month}_normal_distribution.png')
            plt.savefig(output_file)
            plt.close()
            print(f"{month} - {state}的图像已保存到 {output_file}")





def Two_dimensional_normal_2():
    # 读取数据
    df = pd.read_csv('H:\\geo-bias\\summary\\Pennsylvania.csv', dtype={'state': str, 'count': int, 'average': float},
                     header=0)

    print(df.shape[0])

    # 定义区间
    bins = [-3, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3]
    labels = ['[-3, -2.5)', '[-2.5, -1.5)', '[-1.5, -0.5)', '[-0.5, 0.5)', '[0.5, 1.5)', '[1.5, 2.5)', '[2.5, 3]']

    # 将average列按照区间进行划分
    df['interval'] = pd.cut(df['average'], bins=bins, labels=labels, right=False)
    df.loc[df['average'] == 3, 'interval'] = '[2.5, 3]'

    print(df)

    # 计算每个区间的个数和比例
    interval_counts = df['interval'].value_counts().sort_index()
    interval_proportions = df['interval'].value_counts(normalize=True).sort_index()

    # 输出每个区间的个数和比例
    for interval in interval_counts.index:
        print(f"区间 {interval}: 个数 = {interval_counts[interval]}, 比例 = {interval_proportions[interval]:.4f}")

    print(interval_counts)
    print(interval_proportions)

    # 计算加权平均值
    weighted_average = 0
    for interval, proportion in interval_proportions.items():
        if proportion != 0:
            # 计算当前区间内的average的平均值
            interval_mean = df[df['interval'] == interval]['average'].mean()
            print('1', interval_mean * proportion, '=', interval_mean, '*', proportion)
            # 加权平均值
            weighted_average += interval_mean * proportion

    print(f"加权平均值: {weighted_average}")

    # 输出df中的average平均值
    df_average = df['average'].mean()
    print(f"数据集中average的平均值: {df_average:.4f}")

    # 计算加权中位数平均值
    weighted_median_average = 0
    for interval, proportion in interval_proportions.items():
        interval_data = df[df['interval'] == interval]['average']
        interval_median = interval_data.median() if len(interval_data) > 0 else np.nan
        if not np.isnan(interval_median):
            weighted_median_average += interval_median * proportion

    print(f"\n加权中位数平均值: {weighted_median_average:.4f}")

    # 计算并输出数据缩放后的平均值和标准差
    df['scaled_average'] = (df['average'] - (-3)) / (3 - (-3)) * (1 - (-1)) + (-1)

    # 定义缩放后的区间
    scaled_bins = [-1, -5 / 6, -1 / 2, -1 / 6, 1 / 6, 1 / 2, 5 / 6, 1]
    scaled_labels = ['[-1, -5/6)', '[-5/6, -1/2)', '[-1/2, -1/6)', '[-1/6, 1/6)', '[1/6, 1/2)', '[1/2, 5/6)',
                     '[5/6, 1]']

    # 将scaled_average列按照缩放后的区间进行划分
    df['scaled_interval'] = pd.cut(df['scaled_average'], bins=scaled_bins, labels=scaled_labels, right=False)
    df.loc[df['scaled_average'] == 1, 'scaled_interval'] = '[5/6, 1]'

    print(df)

    # 计算缩放后每个区间的个数和比例
    scaled_interval_counts = df['scaled_interval'].value_counts().sort_index()
    scaled_interval_proportions = df['scaled_interval'].value_counts(normalize=True).sort_index()

    # 输出每个缩放区间的个数和比例
    for interval in scaled_interval_counts.index:
        print(
            f"缩放区间 {interval}: 个数 = {scaled_interval_counts[interval]}, 比例 = {scaled_interval_proportions[interval]:.4f}")

    # 计算缩放后加权中位数平均值
    scaled_weighted_median_average = 0
    for interval, proportion in scaled_interval_proportions.items():
        interval_data = df[df['scaled_interval'] == interval]['scaled_average']
        interval_median = interval_data.median() if len(interval_data) > 0 else np.nan
        if not np.isnan(interval_median):
            scaled_weighted_median_average += interval_median * proportion

    print(f"\n缩放后加权中位数平均值: {scaled_weighted_median_average:.4f}")

    # 计算缩放后的平均值和标准差
    scaled_mean = df['scaled_average'].mean()
    scaled_std_dev = df['scaled_average'].std()

    # 生成基于缩放后平均值和标准差的正态分布
    x = np.linspace(-1, 1, df.shape[0])
    y = stats.norm.pdf(x, scaled_mean, scaled_std_dev)

    # 绘制正态分布和数据点的直方图
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label='Normal Distribution', color='blue')
    plt.hist(df['scaled_average'], bins=60, density=True, alpha=0.6, color='g', label='Data Histogram')
    plt.xlabel('Scaled Average')
    plt.ylabel('Density')
    plt.title('Normal Distribution of Scaled Average')
    plt.legend()
    plt.grid(True)
    plt.show()

def stastic_bias_num_Proportion():
    # 定义区间
    bins = [-3, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3]
    labels = ['[-3, -2.5)', '[-2.5, -1.5)', '[-1.5, -0.5)', '[-0.5, 0.5)', '[0.5, 1.5)', '[1.5, 2.5)', '[2.5, 3]']

    # 文件路径
    base_path = 'H:\\geo-bias\\every_mouth'  # 替换为你的文件路径
    output_path = 'H:\\geo-bias\\output'

    # 初始化结果字典
    results = []

    # 遍历每个文件夹
    for folder in sorted(os.listdir(base_path)):
        folder_path = os.path.join(base_path, folder)
        print(folder_path)

        if os.path.isdir(folder_path):
            # 遍历每个州的CSV文件
            for file in sorted(os.listdir(folder_path)):
                if file.endswith('.csv'):
                    file_path = os.path.join(folder_path, file)
                    print(file_path)
                    state = file.replace('.csv', '')
                    print(state)

                    # 读取CSV文件
                    df = pd.read_csv(file_path, dtype={'retweeted_user_id': str, 'average': float}, header=0)

                    # 将average列数据按照区间划分，修正区间划分方式
                    df['bin'] = pd.cut(df['average'], bins=bins, labels=labels, right=False)
                    df.loc[df['average'] == 3, 'bin'] = '[2.5, 3]'

                    # 统计数量及比例
                    count = df['bin'].value_counts().sort_index()
                    total = count.sum()
                    proportion = count / total

                    # 将统计结果添加到results列表中
                    for interval in labels:
                        results.append({
                            'Month': folder,
                            'State': state,
                            'Interval': interval,
                            'Count': count.get(interval, 0),
                            'Proportion': proportion.get(interval, 0)
                        })

    # 将结果转换为DataFrame并保存为CSV
    result_df = pd.DataFrame(results)
    result_df.to_csv(os.path.join(output_path, 'result.csv'), index=False)
    print("结果已保存到CSV文件中。")


def plot_3d_scatter1():
    # 读取生成的CSV文件
    output_path = 'H:\\geo-bias\\ervery_mouth_every_state_bias_num_proportion.csv'  # 替换为你的输出文件路径
    df = pd.read_csv(output_path, header=0)

    selected_states = ['District of Columbia', 'Vermont', 'Massachusetts', 'Maryland', 'California', 'Hawaii', 'New York',
                       'Nevada', 'Michigan', 'Pennsylvania', 'Wisconsin', 'Arizona', 'Georgia', 'North Carolina', 'Florida', 'Ohio',
                       'Tennessee', 'Kentucky', 'Arkansas', 'Idaho', 'South Dakota',  'Alabama',  'North Dakota',  'Oklahoma',  'West Virginia', 'Wyoming'
                       ]
    # 过滤数据，只保留选定的州
    df = df[df['State'].isin(selected_states)]

    # 区间颜色映射
    color_map = {
        '[-3, -2.5)': 'darkred',
        '[-2.5, -1.5)': 'orangered',
        '[-1.5, -0.5)': 'goldenrod',  # 更深的黄色
        '[-0.5, 0.5)': 'limegreen',
        '[0.5, 1.5)': 'dodgerblue',
        '[1.5, 2.5)': 'darkviolet',
        '[2.5, 3]': 'deeppink'
    }

    df['Color'] = df['Interval'].map(color_map)

    # 创建三维散点图
    fig = plt.figure(figsize=(30, 15))
    ax = fig.add_subplot(111, projection='3d')

    # # 获取唯一的州和时间
    # states = df['State'].unique()
    # times = df['Month'].unique()

    # 将州和时间映射到数值，并保持特定顺序
    state_to_num = {state: i * 400 for i, state in enumerate(selected_states)}
    times = df['Month'].unique()
    time_to_num = {time: i * 400 for i, time in enumerate(times)}

    df['State_Num'] = df['State'].map(state_to_num)
    df['Month_Num'] = df['Month'].map(time_to_num)

    colors = df['Color'].values
    scatter = ax.scatter(df['State_Num'], df['Month_Num'], df['Proportion'], c=colors, s=40)

    # 设置坐标轴标签
    ax.set_xlabel('State', labelpad=80)
    ax.set_ylabel('Time', labelpad=20)
    ax.set_zlabel('Proportion', labelpad=20)

    # 设置x轴刻度为州名
    ax.set_xticks(list(state_to_num.values()))
    ax.set_xticklabels(list(state_to_num.keys()), rotation=90)

    # 设置y轴刻度为时间
    ax.set_yticks(list(time_to_num.values()))
    ax.set_yticklabels(list(time_to_num.keys()), rotation=90)

    # 扩大坐标轴的范围
    ax.set_xlim(min(state_to_num.values()) - 400, max(state_to_num.values()) + 400)
    ax.set_ylim(min(time_to_num.values()) - 400, max(time_to_num.values()) + 400)

    # 调整视角
    ax.view_init(elev=20., azim=-60)

    # 设置图例
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[label], markersize=10) for label in
               color_map]
    labels = [f'{label} ({color_map[label]})' for label in color_map.keys()]
    ax.legend(handles, labels, title="State Bias", loc='upper left', bbox_to_anchor=(1.05, 1))



    plt.show()


def plot_3d_scatter2():
    # 读取生成的CSV文件
    output_path = 'H:\\geo-bias\\ervery_mouth_every_state_bias_num_proportion.csv'  # 替换为你的输出文件路径
    df = pd.read_csv(output_path, header=0)

    selected_states = ['District of Columbia', 'Vermont', 'Massachusetts', 'Maryland', 'California', 'Hawaii', 'New York',
                       'Nevada', 'Michigan', 'Pennsylvania', 'Wisconsin', 'Arizona', 'Georgia', 'North Carolina', 'Florida', 'Ohio',
                       'Tennessee', 'Kentucky', 'Arkansas', 'Idaho', 'South Dakota', 'Alabama', 'North Dakota', 'Oklahoma', 'West Virginia', 'Wyoming'
                       ]

    # 过滤数据，只保留选定的州
    df = df[df['State'].isin(selected_states)]

    # 删除区间 [-3, -2.5) 的数据点
    df = df[df['Interval'] != '[-3, -2.5)']

    # 处理 NaN 值
    df = df.dropna(subset=['State', 'Month', 'Proportion', 'Interval'])

    # 更加鲜明的颜色映射
    color_map = {
        '[-3, -2.5)': 'orangered',
        '[-2.5, -1.5)': 'darkred',
        '[-1.5, -0.5)': 'goldenrod',  # 更深的黄色
        '[-0.5, 0.5)': 'limegreen',
        '[0.5, 1.5)': 'dodgerblue',
        '[1.5, 2.5)': 'darkviolet',
        '[2.5, 3]': 'deeppink'
    }

    df['Color'] = df['Interval'].map(color_map)

    # 将州和时间映射到数值，并保持特定顺序
    state_to_num = {state: i * 30 for i, state in enumerate(selected_states)}
    times = df['Month'].unique()
    time_to_num = {time: i * 30 for i, time in enumerate(times)}

    df['State_Num'] = df['State'].map(state_to_num)
    df['Month_Num'] = df['Month'].map(time_to_num)

    # 创建三维散点图
    fig = go.Figure()

    for interval, color in color_map.items():
        subset = df[df['Interval'] == interval]

        fig.add_trace(go.Scatter3d(
            x=subset['State_Num'],
            y=subset['Month_Num'],
            z=subset['Proportion'],
            mode='markers',
            marker=dict(
                size=5,
                color=color,
                opacity=0.5
            ),
            name=interval,  # 使用区间作为图例标签
            legendgroup=interval,  # 分组图例
            showlegend=True,
            hoverinfo='text',
            text=subset['State']  # 悬停时显示的文本
        ))


    # 设置坐标轴标签
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='State', tickvals=list(state_to_num.values()), ticktext=list(state_to_num.keys()), tickangle=-90),
            yaxis=dict(title='Time', tickvals=list(time_to_num.values()), ticktext=list(time_to_num.keys()), tickangle=-90),
            zaxis=dict(title='Proportion', range=[0, 0.7])  # 固定 z 轴的范围
            # zaxis = dict(title='Proportion')  # 不固定 z 轴的范围
        ),
        title='State Bias',
        legend=dict(title="Interval"),
        margin=dict(l=50, r=50, b=50, t=50),  # 调整图的边距
        # height = 800,  # 设置图的高度
        # width = 1200  # 设置图的宽度
        hovermode='closest'  # 设置悬停模式
    )

    # 保存为HTML文件
    fig.write_html('H:\\geo-bias\\d_scatter_plot-with_z.html')
    fig.show()


if __name__ == "__main__":

    # select_id_in_state()
    # statistics_15_mouth()
    # output()
    # summary_average()
    # every_mouth_change()
    Two_dimensional_normal3()
    # print("==================================================================================================================")
    # Two_dimensional_normal_2()
    # stastic_bias_num_Proportion()
    # plot_3d_scatter2()

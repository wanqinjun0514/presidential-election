import os
import pandas as pd

# 文件夹路径
input_folder = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\sankey_plot\common_user_bias'
output_folder = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\sankey_plot\cross_table'

# 创建输出文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# 将average_bias_points值分类为Left, Center, Right
def classify_bias(bias):
    if bias < 0:
        return 'LEFT'
    elif bias == 0:
        return 'CENTER'
    else:
        return 'RIGHT'


# 处理每个CSV文件，计算转变数量
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        # 读取文件
        file_path = os.path.join(input_folder, file_name)
        df = pd.read_csv(file_path)

        # 分类列
        df['month1_category'] = df['average_bias_points_month1'].apply(classify_bias)
        df['month2_category'] = df['average_bias_points_month2'].apply(classify_bias)

        # 创建透视表，统计转变数量
        transition_table = pd.crosstab(df['month1_category'], df['month2_category'])

        # 期望的所有组合
        all_combinations = [('LEFT', 'LEFT'), ('LEFT', 'CENTER'), ('LEFT', 'RIGHT'),
                            ('CENTER', 'LEFT'), ('CENTER', 'CENTER'), ('CENTER', 'RIGHT'),
                            ('RIGHT', 'LEFT'), ('RIGHT', 'CENTER'), ('RIGHT', 'RIGHT')]

        # 构建输出数据框
        output_data = []
        for from_category, to_category in all_combinations:
            count = transition_table.at[from_category, to_category] if (
                        from_category in transition_table.index and to_category in transition_table.columns) else 0
            output_data.append([from_category, to_category, count])

        output_df = pd.DataFrame(output_data, columns=['From', 'To', 'Count'])

        # 保存结果
        output_file_path = os.path.join(output_folder, file_name)
        output_df.to_csv(output_file_path, index=False)
        print(f'{file_name} 处理完成！')

print("所有文件处理完成！")

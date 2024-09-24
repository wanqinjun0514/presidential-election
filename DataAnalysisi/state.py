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


def statistics_state(cvs_path, result_path):
    print(f"内容开始读取!")
    df_cvs = pd.read_csv(cvs_path, header=0, dtype=str, usecols=["retweeted_user_id", "retweeted_user_location"])
    print(f"内容读取成功!")
    # print(df_cvs)

    # 设置显示选项
    pd.set_option('display.max_columns', None)  # 不限制列数
    pd.set_option('display.width', None)  # 根据内容自动调整输出宽度

    cvs_num = df_cvs.shape[0]
    # print(cvs_num)

    # 计算 'retweeted_user_location' 列中 NaN 值的数量
    nan_count = df_cvs['retweeted_user_location'].isna().sum()
    # print(f"'retweeted_user_location' 列中的NaN数量是: {nan_count}")

    # 根据所有列分组，并计算每个组的大小
    counts = df_cvs.groupby(list(df_cvs.columns)).size()

    # 将结果转换为DataFrame并重置索引，以便更清晰地查看
    counts = counts.reset_index(name='Count')
    total_count = counts['Count'].sum()
    # print(counts)
    # print(total_count)

    counts.to_csv(result_path, index=False, header=True)

    return cvs_num, nan_count, total_count


def batch_statistics_state(folder_path, folder_name):
    record_txt = f'H:\\state\\record\\{folder_name}.txt'

    for cvs_name in os.listdir(folder_path):
        print("---------------------------------------------------------------------------------------------------")
        print(cvs_name)
        cvs_path_batch = os.path.join(folder_path, cvs_name)
        # print(cvs_path_batch)

        new_filename = cvs_name.replace("output", "state")
        dir_name = folder_name.replace("output_", "").replace("_", "-")
        dir_path = os.path.join("H:\\state", dir_name)
        # print(dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        result_path_batch = os.path.join(dir_path, new_filename)
        # print(result_path_batch)

        print(cvs_path_batch)
        print(result_path_batch)
        print(record_txt)

        cvs_num, nan_count, total_count = statistics_state(cvs_path_batch, result_path_batch)

        with open(record_txt, 'a', encoding='utf-8') as rt:
            print_string = f"{cvs_name}：cvs_num: {cvs_num}\t\tnan_count: {nan_count}\t\ttotal_count: {total_count}\n"
            rt.write(print_string)


def merge_csv(folder_path, result_path):
    # 读取文件夹中所有CSV文件
    all_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]
    all_data = []  # 用于存储每个文件的DataFrame

    origin_line_num = 0

    for file in all_files:
        # 读取每个CSV文件到DataFrame
        print(file)
        df = pd.read_csv(file, dtype={'retweeted_user_id': 'str', 'retweeted_user_location': 'str', 'Count': 'int64'})
        origin_line_num = origin_line_num + df['Count'].sum()
        all_data.append(df)

    # 合并所有DataFrame到一个单独的DataFrame
    combined_df = pd.concat(all_data, ignore_index=True)

    # 根据'retweeted_user_id'和'retweeted_user_location'分组，并对'Count'求和
    final_df = combined_df.groupby(['retweeted_user_id', 'retweeted_user_location'], as_index=False).sum()

    final_df['retweeted_user_id'] = pd.to_numeric(final_df['retweeted_user_id'], errors='coerce')
    sorted_df = final_df.sort_values(by='retweeted_user_id')

    print(origin_line_num)
    print(sorted_df['Count'].sum())

    # 可以选择将结果保存到新的CSV文件中
    sorted_df.to_csv(result_path, index=False)

    # print(final_df)
    # print(final_df['Count'].sum())


def batch_merge_csv():
    # 合并每个月的csv
    # path = "H:\\state\\data"
    # for name in os.listdir(path):
    #     print("---------------------------------------------------------------------------------------------------")
    #     folder_path = os.path.join(path, name)
    #     print(folder_path)
    #
    #     result_path = os.path.join("H:\\state\\merge", f"{name}.csv")
    #     print(result_path)
    #
    #     merge_csv(folder_path, result_path)

    # 合并所有月份
    merge_csv("H:\\state\\merge", "H:\\state\\final_user_state.csv")


def extract_geo():
    # 加载 Spacy 模型
    nlp = spacy.load('en_core_web_lg')
    # cc = OpenCC('t2s')  # 繁体转简体

    for i in range(27, 28):

        csv_path = f"H:\\state\\location-NlP\\location-NLP-{i}.csv"
        result_path = f"H:\\state\\location-NlP\\location-NLP-{i + 1}.csv"

        # 读取数据
        print("开始读取！")
        df_csv = pd.read_csv(csv_path, header=0,
                             dtype={'Location': 'str', 'Count': 'int', 'entities': 'str', 'language': 'str'})
        print("读取完成！")
        print(df_csv)
        np_csv = df_csv.to_numpy()
        print(np_csv)
        print("转换完成")

        # 初始化一个空列表来存储命名实体
        entities_list = []
        lang_list = []
        all_line = 0

        # 迭代 DataFrame 中的每一行
        for data in np_csv:

            all_line += 1
            if all_line % 50000 == 0:  # 当i是50000的倍数时
                print(f"final_location.csv 处理到行数: {all_line}")

            # print(data)
            loc = data[0]
            ent = data[2]
            lang = data[3]
            if pd.isna(ent):
                # print(loc)
                if lang != 'Error':  # 检查语言是否为英语
                    try:
                        doc = nlp(loc)  # 使用NLP模型处理位置文本
                        entities = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
                        if entities:  # 检查是否找到了实体
                            entities_list.append(entities)
                            lang = 'en'  # 设置语言为英语
                        else:
                            entities_list.append(None)  # 如果没有找到实体，则添加None
                    except Exception as e:  # 通用异常处理
                        print(f"Error processing location: {loc}, Error: {e}")
                        entities_list.append(None)  # 如果处理失败，则添加None
                else:
                    entities_list.append(None)  # 如果文本不是英语，则添加None
            else:
                entities_list.append(ent)  # 如果原始数据中已有实体数据，直接复制过来

            lang_list.append(lang)  # 更新语言列表

        # 将命名实体列表添加为 DataFrame 的一个新列
        df_csv['entities'] = entities_list
        df_csv['language'] = lang_list  # 更新 DataFrame 的语言列
        # # 现在可以查看 DataFrame，或将其保存回 CSV
        # print(df_csv.head())

        df_csv.to_csv(result_path, index=False, header=True)


def cheak_result_NaN():
    csv_path = f"H:\\state\\merge513\\location-NLP-2.csv"
    df_csv = pd.read_csv(csv_path, header=0,
                         dtype={'Location': 'str', 'Count': 'int', 'entities': 'str', 'language': 'str',
                                'State Full Name': 'str'})

    nan_count = df_csv['State Full Name'].isna().sum()
    print("总行数：", df_csv.shape[0])
    print("231万中空行数：", nan_count)

    num1 = df_csv['Count'].sum()
    print("总出现次数：", num1)

    # 筛选State Full Name不为空的行
    filtered_df = df_csv[df_csv['State Full Name'].notna()]
    print("标记出州名的地点df：")
    print(filtered_df)
    num2 = filtered_df['Count'].sum()
    print("标记处州名的地点出现次数：", num2)

    print("标出州名的整体比例", num2/num1)

    # 选取前4000行
    subset_df = df_csv.head(4000)

    # 计算给定列（这里以'Amount'为例）的数值之和
    num3 = subset_df['Count'].sum()
    print("前四千行总出现次数：", num3)
    filtered_subset_df = subset_df[subset_df['State Full Name'].notna()]
    print("前四行标记出州名的地点df：")
    print(filtered_subset_df)
    num4 = filtered_subset_df['Count'].sum()
    print("前四千行标记处州名的地点出现次数：", num4)

    print("前四千行标出州名的整体比例", num4/num3)

    # 重置索引，如果不希望在输出的DataFrame中保留旧的索引，可以使用drop=True
    filtered_df = filtered_df.reset_index(drop=True)
    # 输出到CSV文件
    filtered_df.to_csv('H:\\state\\loc_state_final.csv', index=False)  # index=False表示不将索引列输出到CSV文件中

    # print((df_csv['entities'] == 'non-English').sum())
    #
    # return nan_count

    # csv_path = f"H:\\state\\location-NlP.csv"
    # df_csv = pd.read_csv(csv_path, header=0,
    #                      dtype={'retweeted_user_id': 'str', 'retweeted_user_location': 'str', 'Count': 'int',
    #                             'entities': 'str', 'State Full Name': 'str'})
    #
    # nan_count = df_csv['State Full Name'].isna().sum()
    # print(nan_count)
    #
    # print(df_csv.shape[0] - nan_count)

    # 读取CSV文件

    # # f"H:\\state\\location-NLP.csv"   \\location-NLP-27
    # df = pd.read_csv('H:\\state\\location-NlP.csv', header=0,
    #                  dtype={'Location': 'str', 'Count': 'int', 'entities': 'str', 'language': 'str',
    #                         'State Full Name': 'str'})
    #
    # print((df['language'] == 'en').sum())
    # print(df['Location Detail'].count())


def select_none_entities():
    # 读取CSV文件
    df = pd.read_csv(f"H:\\state\\location-NlP\\location-NLP-27.csv", header=0,
                     dtype={'Location': 'str', 'Count': 'int', 'entities': 'str', 'language': 'str', })

    # 筛选出指定列为NaN的行
    filtered_df = df[df['entities'].isna()]

    # 保存到新的CSV文件
    filtered_df.to_csv(f"H:\\state\\location-NlP\\none_entities.csv", index=False)


def check_states_in_csv():
    df = pd.read_csv(f"H:\\state\\location-NlP\\none_entities.csv", header=0,
                     dtype={'Location': 'str', 'Count': 'int', 'entities': 'str', 'language': 'str'})

    # 美国所有州的全称和简称
    states_full = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
                   "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
                   "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
                   "Missouri",
                   "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
                   "North Carolina",
                   "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
                   "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
                   "Wisconsin", "Wyoming"]
    states_abbr = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
                   "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND",
                   "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    # 合并并转换为小写以进行不区分大小写的比较
    states_combined = states_full + states_abbr
    states_combined = set([state.lower() for state in states_combined])

    # 筛选包含州名或缩写的行
    filtered_df = df[df['Location'].str.lower().isin(states_combined)]

    # 保存筛选后的数据到新的CSV文件
    filtered_df.to_csv(f"H:\\state\\location-NlP\\none_entities_in_states.csv", index=False)


def disassemble_state_county():
    df_1 = pd.read_csv("H:\\state\\state-county.csv", header=0, dtype={'NAME': 'str', 'state': 'str', 'county': 'str'})
    df_2 = pd.read_csv("H:\\state\\US_States_and_Abbreviations.csv", header=0,
                       dtype={'State': 'str', 'Abbreviation': 'str'})
    print(df_1)
    print(df_2)

    df_1[['County', 'State']] = df_1['NAME'].str.rsplit(', ', n=1, expand=True)
    print(df_1)

    df_result = df_1[['State', 'County']]
    print(df_result)

    merge_df = pd.merge(df_result, df_2, how="left", on="State")
    print(merge_df)

    merge_df.to_csv("H:\\state\\location-NlP\\state-county-abbreviation.csv", index=False)


def cheak_us_locations_entity():
    # 设置显示选项
    pd.set_option('display.max_columns', None)  # 不限制列数
    pd.set_option('display.width', None)  # 根据内容自动调整输出宽度

    print("开始读取！")
    states_df = pd.read_csv("H:\\state\\state-county-abbreviation.csv", header=0, dtype=str)
    locations_df = pd.read_csv(f"H:\\state\\location-NlP\\location-NLP-27.csv", header=0,
                               dtype={'Location': 'str', 'Count': 'int', 'entities': 'str', 'language': 'str'})
    print("读取完成！")
    print(states_df)
    print(locations_df)

    # new_arr = np_nlp[:10, :]
    #
    # for data in new_arr:
    #     loc_list = ast.literal_eval(data[2])
    #     print(loc_list)
    #     for loc_tuple in loc_list:
    #         loc = loc_tuple[0]
    #         print(loc)

    # 函数用于从 entities 列中提取所有实体名称
    def extract_entities(entities_str):
        import ast
        entities = ast.literal_eval(entities_str)
        return [entity[0] for entity in entities]

    # 检查每一行的 entities 是否匹配美国州名，并添加州全名
    def match_states(row):
        if pd.isna(row['entities']):
            return None
        entities = extract_entities(row['entities'])
        print(entities)
        for entity in entities:
            matched_state = states_df[(states_df['State'].str.lower() == entity.lower()) |
                                      (states_df['County'].str.lower() == entity.lower()) |
                                      (states_df['Abbreviation'].str.lower() == entity.lower())]['State'].unique()
            print(matched_state)
            if matched_state.size > 0:
                return matched_state[0]
        return None

    # 应用 match_states 函数到每行
    locations_df['State Full Name'] = locations_df.apply(match_states, axis=1)

    # 保存处理后的 DataFrame 到新的 CSV 文件
    locations_df.to_csv("H:\\state\\location-NLP.csv", index=False)


def cheak_us_locations_Location():
    # 设置显示选项
    pd.set_option('display.max_columns', None)  # 不限制列数
    pd.set_option('display.width', None)  # 根据内容自动调整输出宽度

    print("开始读取！")
    states_df = pd.read_csv("H:\\state\\state-county-abbreviation.csv", header=0, dtype=str)
    locations_df = pd.read_csv(f"H:\\state\\location-NlP\\none_entities.csv", header=0,
                               dtype={'Location': 'str', 'Count': 'int', 'entities': 'str', 'language': 'str'})
    print("读取完成！")
    print(states_df)
    print(locations_df)

    line_num = 0

    # 定义内部匹配函数
    def match_location(location):

        nonlocal line_num
        line_num += 1
        print(line_num)

        if pd.isna(location):
            return None  # 如果位置是 NaN，则返回 None

        # 检查位置是否与任何州名直接匹配
        state_match = states_df[states_df['State'].str.lower() == location.lower()]['State'].unique()
        if len(state_match) > 0:
            return state_match[0]

        # 检查位置是否包含任何县名
        for index, row in states_df.iterrows():
            if row['County'].replace(" County", "").lower() in location.lower():
                return row['State']

        # 检查位置是否与任何州的简称匹配
        abbreviation_match = states_df[states_df['Abbreviation'].str.lower() == location.lower()][
            'State'].unique()
        if len(abbreviation_match) > 0:
            return abbreviation_match[0]

        return None  # 如果没有找到匹配，则返回 None

    # 应用匹配函数并添加新列
    locations_df['State Full Name'] = locations_df['Location'].apply(match_location)
    # 保存处理后的 DataFrame 到新的 CSV 文件
    locations_df.to_csv("H:\\state\\location-NLP-none_entities.csv", index=False)


def cheak_us_locations_geo():
    # # 加载美国各州的地理数据
    # usa = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    # usa = usa[usa['continent'] == 'North America']  # 限制为北美地区
    #
    # 载入第二个 CSV 文件
    locations_df = pd.read_csv(f"H:\\state\\location-NLP-none_entities-geo-1.csv", header=0,
                               dtype={'Location': 'str', 'Count': 'int', 'entities': 'str', 'language': 'str',
                                      'State Full Name': 'str', 'Location Detail': 'str'})

    # # 将 Location 列转换为点坐标
    # def parse_coordinates(location):
    #     try:
    #         if '/' not in location:
    #             return None
    #         lat_part, lon_part = location.split('/')
    #         print(lat_part, lon_part)
    #         lat_dir, lat_deg = lat_part.strip().split(' ', 1)
    #         lon_dir, lon_deg = lon_part.strip().split(' ', 1)
    #
    #         # 解析度数
    #         lat = float(lat_deg.replace('°', '').replace("'", '').replace('"', '').strip())
    #         lon = float(lon_deg.replace('°', '').replace("'", '').replace('"', '').strip())
    #
    #         # 根据方向调整正负
    #         if lat_dir == 'S':
    #             lat = -lat
    #         if lon_dir == 'W':
    #             lon = -lon
    #
    #         point = Point(lon, lat)
    #         return point
    #     except:
    #         return None
    #
    # locations_df['geometry'] = locations_df['Location'].apply(parse_coordinates)
    # geo_second_data = gpd.GeoDataFrame(locations_df, geometry='geometry')
    #
    # # 判断点是否在美国的某个州内
    # def check_in_usa(point):
    #     if point is not None:
    #         for index, row in usa.iterrows():
    #             if row['geometry'].contains(point):
    #                 return row['name']
    #     return None
    #
    # geo_second_data['State Full Name'] = geo_second_data['geometry'].apply(check_in_usa)
    #
    # # 保存处理后的 DataFrame 到新的 CSV 文件
    # locations_df.to_csv("H:\\state\\location-NLP-none_entities-geo.csv", index=False)

    # # 正则表达式，匹配度分秒格式和方向
    # regex = r"^[NS] \d+°\d+' \d+'' / [EW] \d+°\d+' \d+''$"
    #
    # # 应用正则表达式筛选符合格式的行
    # df_filtered = locations_df[locations_df['Location'].apply(lambda x: bool(re.match(regex, x)))]
    # print(df_filtered)
    # df_filtered.reset_index(drop=True)

    geolocator = Nominatim(user_agent="geoapiExercises")

    # def get_location(row):
    #     try:
    #         # 将经纬度格式转换为可用于查询的格式
    #         location = geolocator.reverse(row['Location'].replace("''", '"'), timeout=10)
    #         print(location)
    #         if location:
    #             address = location.raw.get('address', {})
    #             country = address.get('country', '')
    #             state = address.get('state', '')
    #
    #             # 如果地点在美国，更新State Full Name列
    #             if country == "United States of America":
    #                 return state
    #             else:
    #                 # 否则返回国家名供新列使用
    #                 return country
    #         return None
    #     except GeocoderTimedOut:
    #         return "Timeout"
    #
    # # 应用地理编码函数
    # locations_df['Location Detail'] = locations_df.apply(get_location, axis=1)

    def get_state_if_usa(row):
        if row['Location Detail'] == "United States":
            try:
                # 将经纬度格式转换为可用于查询的格式
                location = geolocator.reverse(row['Location'].replace("''", '"'), timeout=10)
                if location:
                    address = location.raw.get('address', {})
                    state = address.get('state', '')
                    return state
            except GeocoderTimedOut:
                return "Timeout"
        return row['State Full Name']

    # 应用地理编码函数
    locations_df['State Full Name'] = locations_df.apply(get_state_if_usa, axis=1)

    print(locations_df)

    # 保存处理后的 DataFrame 到新的 CSV 文件
    locations_df.to_csv("H:\\state\\location-NLP-none_entities-geo-2.csv", index=False)


def slsect_State_notna():
    df = pd.read_csv(f"H:\\state\\location-NLP.csv", header=0,
                     dtype={'Location': 'str', 'Count': 'int', 'entities': 'str', 'language': 'str',
                            'State Full Name': 'str'})

    # 检查指定列非空的行
    new_df = df[df['State Full Name'].notna()]

    print(new_df)

    new_df.to_csv("H:\\state\\location-NLP-none_entities-geo-3.csv", index=False)


def cheak_gpe_loc_org():
    df = pd.read_csv('H:\\state\\location-NlP.csv', header=0,
                     dtype={'Location': 'str', 'Count': 'int', 'entities': 'str', 'language': 'str',
                            'State Full Name': 'str'})

    # 创建一个新的DataFrame
    new_df = pd.DataFrame(columns=df.columns)
    all_line = 0

    # 遍历数据
    for index, row in df.iterrows():

        all_line += 1
        if all_line % 50000 == 0:  # 当i是50000的倍数时
            print(f"final_location.csv 处理到行数: {all_line}")

        if pd.isna(row['State Full Name']):
            try:
                entities = ast.literal_eval(row['entities'])
                # 检查entities中的每个元组
                for entity in entities:
                    if entity[3] in ['GPE', 'LOC', 'ORG']:
                        print(entities)
                        new_df = new_df._append(row, ignore_index=True)  # 使用ignore_index=True并赋值回new_df
                        break
            except:
                continue  # 如果entities列格式不正确或无法解析，跳过该行

    # 输出新的DataFrame
    print(new_df)

    new_df.to_csv("H:\\state\\location-NlP-gpe-loc-org.csv", index=False)


def cheak_language():
    i = 5
    csv_path = f"H:\\state\\location-NlP\\location-NLP-{i}.csv"
    result_path = f"H:\\state\\location-NlP\\location-NLP-{i + 1}.csv"

    # 读取数据
    print("开始读取！")
    df_csv = pd.read_csv(csv_path, header=0, dtype={'Location': 'str', 'Count': 'int', 'entities': 'str'})
    print("读取完成！")
    print(df_csv)
    np_csv = df_csv.to_numpy()
    print(np_csv)
    print("转换完成")

    language_list = []
    language_count = {}
    all_line = 0

    for data in np_csv:

        all_line += 1
        if all_line % 50000 == 0:  # 当i是50000的倍数时
            print(f"final_location.csv 处理到行数: {all_line}")

        loc = data[0]
        # print(loc)
        try:
            language_code = detect(loc)
            language_list.append(language_code)
            if language_code in language_count:
                language_count[language_code] += 1
            else:
                language_count[language_code] = 1
        except Exception as e:
            print(f"Error detecting language: {e}")
            language_list.append('Error')
            if 'Error' in language_count:
                language_count['Error'] += 1
            else:
                language_count['Error'] = 1

    print("语言检测结果和次数统计:")
    for lang, count in language_count.items():
        print(f"{lang}: {count}")

    df_csv['language'] = language_list
    # print(language_list)

    df_csv.to_csv(result_path, index=False, header=True)


def question():
    folder_path = "H:\\state\\data\\2020-01"
    all_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]
    all_data = []  # 用于存储每个文件的DataFrame

    for file in all_files:
        # 读取每个CSV文件到DataFrame
        print(
            "-----------------------------------------------------------------------------------------------------------------")
        print(file)
        df = pd.read_csv(file, dtype={'retweeted_user_id': 'str', 'retweeted_user_location': 'str', 'Count': 'str'})
        all_data.append(df)

    # 合并所有DataFrame到一个单独的DataFrame
    combined_df = pd.concat(all_data, ignore_index=True)

    # 根据'retweeted_user_id'和'retweeted_user_location'分组，并对'Count'求和
    final_df = combined_df.groupby(['retweeted_user_id', 'retweeted_user_location'], as_index=False).sum()

    final_df['retweeted_user_id'] = pd.to_numeric(final_df['retweeted_user_id'], errors='coerce')
    sorted_df = final_df.sort_values(by='retweeted_user_id')
    # 可以选择将结果保存到新的CSV文件中
    sorted_df.to_csv("H:\\state\\2020-01.csv", index=False)

    #     # 假设我们要找的字符串是'berry'
    #     search_string = 'https://twitter.com/janearraf/status/1213823941321592834'
    #
    #     # 将DataFrame中的数据转换为字符串，并使用str.contains()查找指定字符串
    #     mask = df.apply(lambda x: x.str.contains(search_string))
    #
    #     # 打印包含指定字符串的结果
    #     print(df[mask.any(axis=1)])

    # df = pd.read_csv("H:\\us-presidential-output\\output_2020_01\\2020-01-06-1-output.csv", dtype=str, header=0)
    #
    # # 检查指定列中的值是否等于特定字符串
    # matches = df['retweeted_user_location'] == 'https://twitter.com/janearraf/status/1213823941321592834'
    #
    # # 打印结果
    # print(matches)
    #
    # # 可以使用这个布尔型序列来筛选出满足条件的行
    # filtered_df = df[matches]
    # print(filtered_df)

    # cvs_num, nan_count, total_count = statistics_state("H:\\us-presidential-output\\output_2020_01\\2020-01-06-1-output.csv", "H:\\state\\data\\2020-01-06-1-state.csv")
    # print(cvs_num, nan_count, total_count)


def merger_and_remove_duplicates_location():
    csv_path = "H:\\state\\final_user_state.csv"
    print("开始读取！")
    df = pd.read_csv(csv_path, dtype={'retweeted_user_id': 'str', 'retweeted_user_location': 'str', 'Count': 'int64'})
    print("读取完成！")

    location_df = df['retweeted_user_location'].value_counts().reset_index()

    location_df.columns = ['Location', 'Count']
    print(location_df)

    location_df.to_csv("H:\\state\\final_location.csv", index=False, header=True)


def split_csv():
    file_path = "H:\\state\\location-NlP-gpe-loc-org\\location-NlP-gpe-loc-org.csv"
    rows_per_file = 100000
    # 读取大型CSV文件
    reader = pd.read_csv(file_path, chunksize=rows_per_file, dtype=str, header=0)

    # 对每个chunk进行处理
    for i, chunk in enumerate(reader):
        # 生成新的CSV文件名
        new_file = f'H:\\state\\location-NlP-gpe-loc-org\\split_{i + 1}.csv'
        # 保存chunk到新文件
        chunk.to_csv(new_file, index=False)
        print(f'Saved {new_file}')


def merge_geo():
    # df_NLP = pd.read_csv("H:\\state\\location-NLP.csv", header=0, dtype=str)
    # df_geo = pd.read_csv("H:\\state\\geo-final.csv", header=0, dtype=str)
    # df_NLP = pd.read_csv("H:\\state\\merge513\\location-NLP-geo.csv", header=0, dtype=str)
    # df_loc = pd.read_csv("H:\\state\\location-final.csv", header=0, dtype=str)

    df_NLP = pd.read_csv("H:\\state\\merge513\\location-NLP-1.csv", header=0, dtype=str)
    df_loc = pd.read_csv("H:\\state\\location-NlP-gpe-loc-org\\location-NlP-gpe-loc-org(1).csv", header=0, dtype=str)

    # 筛选State Full Name不为空的行
    filtered_df = df_loc[df_loc['State Full Name'].notna()]

    # 将Location设置为索引并转换State Full Name到字典
    location_to_state = filtered_df.set_index('Location')['State Full Name'].to_dict()
    print(location_to_state)
    print(len(location_to_state))

    # 对第一个DataFrame进行处理
    def update_state(row):
        if pd.isna(row['State Full Name']) and row['Location'] in location_to_state:
            return location_to_state[row['Location']]
        else:
            return row['State Full Name']

    # 应用函数更新State Full Name列
    df_NLP['State Full Name'] = df_NLP.apply(update_state, axis=1)

    # 将更新后的DataFrame保存回CSV
    df_NLP.to_csv("H:\\state\\merge513\\location-NLP-2.csv", index=False)

def match_loc_state():
    # 读取CSV文件
    df1 = pd.read_csv('H:\\state\\loc_state_final.csv', header=0, dtype=str)  # 假设第一个文件名为file1.csv
    df2 = pd.read_csv('H:\\state\\final_user_state.csv', header=0, dtype=str)  # 假设第二个文件名为file2.csv

    # 重命名列，使其更清晰
    df1 = df1.rename(columns={'Location': 'location', 'State Full Name': 'state_full_name'})

    # 创建一个新列 'state' 在 df2 中
    df2['state'] = None  # 初始化为空

    print(df1)
    print(df2)

    num = 0

    # # 对于df2中的每一行，检查与df1的location匹配，并填充state
    # for idx, row in df2.iterrows():
    #     num += 1
    #     if num % 500 == 0:  # 当i是50000的倍数时
    #         print(f"行数: {num}")
    #     # 检查每个location是否包含在retweeted_user_location中
    #     mask = df1['location'].apply(lambda x: x in row['retweeted_user_location'])
    #     # 如果存在匹配，从df1中获取state_full_name填充到df2的state列
    #     if mask.any():
    #         df2.at[idx, 'state'] = df1.loc[mask, 'state_full_name'].values[0]

    # 创建一个从location到state_full_name的映射字典
    location_to_state = pd.Series(df1['state_full_name'].values, index=df1['location']).to_dict()
    # print(location_to_state)

    # 使用tqdm来显示进度
    tqdm.pandas(desc="Mapping locations to states")
    df2['state'] = df2['retweeted_user_location'].progress_map(lambda x: location_to_state.get(x, None))

    # 保存更改后的DataFrame为新的CSV文件
    df2.to_csv('H:\\state\\updated_file2.csv', index=False)

def cheak_final_result():

    # 设置显示选项
    pd.set_option('display.max_columns', None)  # 不限制列数
    pd.set_option('display.width', None)  # 根据内容自动调整输出宽度

    df = pd.read_csv('H:\\state\\geo-final-result\\geo-final-result.csv', header=0,
                     dtype={'retweeted_user_id': 'str', 'retweeted_user_location': 'str', 'Count': 'int', 'state': 'str'})

    print(df['state'].isna().sum())
    print(df['state'].notna().sum())

    # 去除首尾空格
    df['state'] = df['state'].str.strip()

    # 统计不同值及其出现的次数
    value_counts = df['state'].value_counts()
    # 打印结果
    print(value_counts)
    print(value_counts.sum())

    # # 筛选包含指定字符串的行
    # filtered_df = df[df['state'].str.contains('California', na=False)]
    #
    # # 临时设置显示选项以打印完整的DataFrame
    # # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    # print(filtered_df)
    #
    # # 替换指定列中的指定值
    # df['state'] = df['state'].replace('New York New Jersey', 'New York')
    # # df['state'] = df['state'].replace('Florida', 'Florida')
    #
    # df.to_csv('H:\\state\\geo-final-result\\geo-final-result-3.csv', index=False)

    # # 创建保存 CSV 文件的文件夹
    # output_folder = 'H:\\state\\geo-final-result\\state'
    # os.makedirs(output_folder, exist_ok=True)
    #
    # # 根据 state 列分组，并为每个组创建一个单独的 CSV 文件
    # for state, group in df.groupby('state'):
    #     # # 去除文件名中的空格和特殊字符
    #     # state_cleaned = state.replace(" ", "_").replace("/", "_").replace("\\", "_")
    #     output_file = os.path.join(output_folder, f'{state}.csv')
    #     group.to_csv(output_file, index=False)
    #
    # print("CSV 文件已成功创建并保存到指定文件夹中。")

if __name__ == "__main__":
    # path = "H:\\us-presidential-output"
    # for root, dirs, files in os.walk(path):
    #     for name in dirs:
    #         folder = os.path.join(root, name)
    #         print("===================================================================================================")
    #         print(name)
    #         batch_statistics_state(folder, name)

    # statistics_state("H:\\demo_data\\2019-12-01-2-output.csv", "H:\\demo_data\\4-15.csv")

    # 测试但是文本情况
    # nlp = spacy.load('en_core_web_sm')
    # doc = nlp("Los Angeles")
    # for ent in doc.ents:
    #     print(ent.text, ent.start_char, ent.end_char, ent.label_)

    # batch_merge_csv()

    # question()

    # merger_and_remove_duplicates_location()

    # num = 27
    # extract_geo()
    # num1 = cheak_result_NaN(num)
    # num2 = cheak_result_NaN(num + 1)
    # print(num1 - num2)
    #
    # select_none_entities()

    # text = langid.classify("Los Angeles, CA")
    # print(text[0])
    #
    # print(detect("Los Angeles, CA"))

    # cheak_language()

    # check_states_in_csv()
    # disassemble_state_county()
    # cheak_us_locations()
    # cheak_us_locations_entity()
    # cheak_result_NaN()
    # cheak_us_locations_geo()
    # slsect_State_notna()
    # cheak_gpe_loc_org()
    # split_csv()

    # merge_geo()
    # cheak_result_NaN()
    # match_loc_state()
    cheak_final_result()

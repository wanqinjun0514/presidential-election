import os
import pandas as pd
from collections import Counter
import json
import csv
#统计所有F:\us-presidential-output\without_url文件夹下的每个月份的原帖用户id-原帖用户名-count的数据
def aggregate_retweet_counts(folder_path, output_file):
    retweet_counts = Counter()
    user_id_to_name = {}

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):

            file_path = os.path.join(folder_path, filename)
            print('正在处理文件：', file_path)
            # Read the CSV file, ensuring all data is read as strings
            df = pd.read_csv(file_path, dtype=str)

            # Ensure 'retweet_origin_user_id' and 'retweet_origin_username' columns exist
            if 'retweet_origin_user_id' in df.columns and 'retweet_origin_username' in df.columns:
                valid_rows = df.dropna(subset=['retweet_origin_user_id',
                                               'retweet_origin_username'])  # Drop rows where either column is NaN
                valid_rows = valid_rows[(valid_rows['retweet_origin_user_id'] != '') & (valid_rows[
                                                                                            'retweet_origin_username'] != '')]  # Drop rows where either column is an empty string

                retweet_counts.update(valid_rows['retweet_origin_user_id'])

                # Update user_id_to_name dictionary
                for user_id, username in zip(valid_rows['retweet_origin_user_id'],
                                             valid_rows['retweet_origin_username']):
                    if user_id not in user_id_to_name:
                        user_id_to_name[user_id] = username

            # Create the DataFrame with retweet_origin_user_id, retweet_origin_username, and count
        result_data = []
        for user_id, count in retweet_counts.items():
            result_data.append([user_id, user_id_to_name.get(user_id, ''), count])

        retweet_counts_df = pd.DataFrame(result_data,
                                         columns=['retweet_origin_user_id', 'retweet_origin_username', 'count'])

        # Save the DataFrame to a new CSV file
        retweet_counts_df.to_csv(output_file, index=False)
#将上面数据合并，且从高到低排序
def combine_aggregate_retweet_counts():
    # 定义文件夹路径和输出文件路径
    folder_path = r'F:\without_url_retweet_user_counts'
    output_file = r'F:\without_url_retweet_user_counts\combined.csv'

    # 初始化一个空的数据框架
    combined_df = pd.DataFrame()

    # 遍历文件夹中的所有CSV文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            # 读取CSV文件
            df = pd.read_csv(file_path)
            # 将当前CSV文件的数据累加到combined_df中
            if combined_df.empty:
                combined_df = df
            else:
                combined_df = pd.concat([combined_df, df])

    # 根据'retweet_origin_user_id'进行分组，累加'count'列的值
    result_df = combined_df.groupby(['retweet_origin_user_id', 'retweet_origin_username'], as_index=False)[
        'count'].sum()

    # 根据'count'列从高到低排序
    result_df = result_df.sort_values(by='count', ascending=False)

    # 将结果保存到新的CSV文件中
    result_df.to_csv(output_file, index=False)

    print(f'Combined and sorted data has been saved to {output_file}')

###F:\without_url_retweet_user_counts\combine_without_url_retweet_user_counts.csv文件，现在需要统计所有count的总和，并且统计出前多少条数据的count之和可以分别达到所有count的总和的60%、70%、80%、90%
# 运行的结果是：
#Total count sum: 286710591，一共有2168879条数据（没有url部分的原帖用户一共是有216万个）
# To reach 60.0% of total count sum, we need top 270 entries.
# To reach 70.0% of total count sum, we need top 737 entries.
# To reach 80.0% of total count sum, we need top 2465 entries.
# To reach 90.0% of total count sum, we need top 14313 entries.
def find_60_70_80_90_percent_data():
    # 定义文件路径
    file_path = 'F:/without_url_retweet_user_counts/combine_without_url_retweet_user_counts.csv'

    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 计算所有count的总和
    total_count_sum = df['count'].sum()

    # 定义目标比例
    ratios = [0.6, 0.7, 0.8, 0.9]

    # 初始化结果字典
    results = {}

    # 计算累积和，并找到满足各比例所需的条数
    cumulative_sum = 0
    for i, count in enumerate(df['count']):
        cumulative_sum += count
        for ratio in ratios:
            if ratio not in results and cumulative_sum >= total_count_sum * ratio:
                results[ratio] = i + 1

    # 打印结果
    print(f'Total count sum: {total_count_sum}')
    for ratio in ratios:
        print(f'To reach {ratio * 100}% of total count sum, we need top {results[ratio]} entries.')



def format_json():
    # 示例JSON数据
    json_data = '''{"created_at": "Sun Dec 01 20:34:18 +0000 2019", "id": 1201238110878797824,
                 "id_str": "1201238110878797824",
                 "full_text": "RT @TomFitton: FLASHBACK: MORE Classified Material Found on Hillary Clinton's Email Server, thanks to @JudicialWatch heavy lifting--@RealDo…",
                 "truncated": false, "display_text_range": [0, 140], "entities": {"hashtags": [], "symbols": [],
                                                                                  "user_mentions": [
                                                                                      {"screen_name": "TomFitton",
                                                                                       "name": "Tom Fitton",
                                                                                       "id": 18266688,
                                                                                       "id_str": "18266688",
                                                                                       "indices": [3, 13]},
                                                                                      {"screen_name": "JudicialWatch",
                                                                                       "name": "Judicial Watch ⚖️",
                                                                                       "id": 18247062,
                                                                                       "id_str": "18247062",
                                                                                       "indices": [102, 116]}],
                                                                                  "urls": []},
                 "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
                 "in_reply_to_status_id": null, "in_reply_to_status_id_str": null, "in_reply_to_user_id": null,
                 "in_reply_to_user_id_str": null, "in_reply_to_screen_name": null,
                 "user": {"id": 1170762655994470400, "id_str": "1170762655994470400", "name": "🍊🍊Oklahoma Bob🍊🍊",
                          "screen_name": "RobertY63542590", "location": "",
                          "description": "🍊🍊MAGA TRUMP 2024 proud deplorable Pro life🍊🍊", "url": null,
                          "entities": {"description": {"urls": []}}, "protected": false, "followers_count": 5006,
                          "fast_followers_count": 0, "normal_followers_count": 5006, "friends_count": 5120,
                          "listed_count": 2, "created_at": "Sun Sep 08 18:16:07 +0000 2019", "favourites_count": 27399,
                          "utc_offset": null, "time_zone": null, "geo_enabled": true, "verified": false,
                          "statuses_count": 33503, "media_count": 3757, "lang": null, "contributors_enabled": false,
                          "is_translator": false, "is_translation_enabled": false, "profile_background_color": "F5F8FA",
                          "profile_background_image_url": null, "profile_background_image_url_https": null,
                          "profile_background_tile": false,
                          "profile_image_url": "http://pbs.twimg.com/profile_images/1228055833516400644/98i7S9PV_normal.jpg",
                          "profile_image_url_https": "https://pbs.twimg.com/profile_images/1228055833516400644/98i7S9PV_normal.jpg",
                          "profile_link_color": "1DA1F2", "profile_sidebar_border_color": "C0DEED",
                          "profile_sidebar_fill_color": "DDEEF6", "profile_text_color": "333333",
                          "profile_use_background_image": true, "has_extended_profile": true, "default_profile": true,
                          "default_profile_image": false, "pinned_tweet_ids": [], "pinned_tweet_ids_str": [],
                          "has_custom_timelines": false, "can_media_tag": true, "followed_by": false,
                          "following": false, "follow_request_sent": false, "notifications": false,
                          "advertiser_account_type": "none", "advertiser_account_service_levels": [],
                          "analytics_type": "disabled", "business_profile_state": "none", "translator_type": "none",
                          "withheld_in_countries": [], "require_some_consent": false}, "geo": null, "coordinates": null,
                 "place": null, "contributors": null,
                 "retweeted_status": {"created_at": "Sun Dec 01 20:07:23 +0000 2019", "id": 1201231336809390080,
                                      "id_str": "1201231336809390080",
                                      "full_text": "FLASHBACK: MORE Classified Material Found on Hillary Clinton's Email Server, thanks to @JudicialWatch heavy lifting--@RealDonaldTrump should ask where's the DOJ?  https://t.co/9Br5kzsLPB https://t.co/waHhEPU0u2",
                                      "truncated": false, "display_text_range": [0, 186],
                                      "entities": {"hashtags": [], "symbols": [], "user_mentions": [
                                          {"screen_name": "JudicialWatch", "name": "Judicial Watch ⚖️", "id": 18247062,
                                           "id_str": "18247062", "indices": [87, 101]},
                                          {"screen_name": "realDonaldTrump", "name": "Donald J. Trump", "id": 25073877,
                                           "id_str": "25073877", "indices": [117, 133]}], "urls": [
                                          {"url": "https://t.co/9Br5kzsLPB",
                                           "expanded_url": "https://judicialwatch.org/press-room/press-releases/judicial-watch-uncovers-more-classified-material-on-hillary-clintons-unsecure-email-system/",
                                           "display_url": "judicialwatch.org/press-room/pre…", "indices": [163, 186]}],
                                                   "media": [
                                                       {"id": 1050395399771619328, "id_str": "1050395399771619328",
                                                        "indices": [187, 210],
                                                        "media_url": "http://pbs.twimg.com/media/DpP3OvBXgAEEqCB.jpg",
                                                        "media_url_https": "https://pbs.twimg.com/media/DpP3OvBXgAEEqCB.jpg",
                                                        "url": "https://t.co/waHhEPU0u2",
                                                        "display_url": "pic.twitter.com/waHhEPU0u2",
                                                        "expanded_url": "https://twitter.com/TomFitton/status/1201231336809390080/video/1",
                                                        "type": "photo", "original_info": {"width": 640, "height": 360},
                                                        "sizes": {"thumb": {"w": 150, "h": 150, "resize": "crop"},
                                                                  "large": {"w": 640, "h": 360, "resize": "fit"},
                                                                  "medium": {"w": 640, "h": 360, "resize": "fit"},
                                                                  "small": {"w": 640, "h": 360, "resize": "fit"}},
                                                        "source_user_id": 18247062, "source_user_id_str": "18247062",
                                                        "features": {}}]}, "extended_entities": {"media": [
                         {"id": 1050395399771619328, "id_str": "1050395399771619328", "indices": [187, 210],
                          "media_url": "http://pbs.twimg.com/media/DpP3OvBXgAEEqCB.jpg",
                          "media_url_https": "https://pbs.twimg.com/media/DpP3OvBXgAEEqCB.jpg",
                          "url": "https://t.co/waHhEPU0u2", "display_url": "pic.twitter.com/waHhEPU0u2",
                          "expanded_url": "https://twitter.com/TomFitton/status/1201231336809390080/video/1",
                          "type": "video", "original_info": {"width": 640, "height": 360},
                          "sizes": {"thumb": {"w": 150, "h": 150, "resize": "crop"},
                                    "large": {"w": 640, "h": 360, "resize": "fit"},
                                    "medium": {"w": 640, "h": 360, "resize": "fit"},
                                    "small": {"w": 640, "h": 360, "resize": "fit"}}, "source_user_id": 18247062,
                          "source_user_id_str": "18247062",
                          "video_info": {"aspect_ratio": [16, 9], "duration_millis": 394194, "variants": [
                              {"bitrate": 288000, "content_type": "video/mp4",
                               "url": "https://video.twimg.com/amplify_video/1050395399771619328/vid/320x180/90jrJJJz6CNLINVH.mp4?tag=8"},
                              {"bitrate": 832000, "content_type": "video/mp4",
                               "url": "https://video.twimg.com/amplify_video/1050395399771619328/vid/640x360/jcKIx5ai5hpRamPX.mp4?tag=8"},
                              {"content_type": "application/x-mpegURL",
                               "url": "https://video.twimg.com/amplify_video/1050395399771619328/pl/JM-G7rhdBXHuunn8.m3u8?tag=8"},
                              {"bitrate": 2176000, "content_type": "video/mp4",
                               "url": "https://video.twimg.com/amplify_video/1050395399771619328/vid/1280x720/5NSNZAIBAKVnrksb.mp4?tag=8"}]},
                          "features": {}, "media_key": "13_1050395399771619328", "ext_alt_text": null,
                          "additional_media_info": {
                              "title": "Tom Fitton - WMAL DC - Will Hillary Clinton Ever Be Prosecuted?",
                              "description": "", "call_to_actions": {"visit_site": {"url": "http://jwatch.us/j9jrw7"}},
                              "embeddable": true, "monetizable": false,
                              "source_user": {"id": 18247062, "id_str": "18247062", "name": "Judicial Watch ⚖️",
                                              "screen_name": "JudicialWatch", "location": "Washington, DC",
                                              "description": "A conservative non-partisan educational foundation promoting transparency, accountability, & integrity in government. Follow us on FB & Instagram: judicialwatch",
                                              "url": "https://t.co/5jmPRuECas", "entities": {"url": {"urls": [
                                      {"url": "https://t.co/5jmPRuECas", "expanded_url": "http://jwatch.us/prmMwg",
                                       "display_url": "jwatch.us/prmMwg", "indices": [0, 23]}]}, "description": {
                                      "urls": []}}, "protected": false, "followers_count": 2129901,
                                              "fast_followers_count": 0, "normal_followers_count": 2129901,
                                              "friends_count": 1730, "listed_count": 6233,
                                              "created_at": "Fri Dec 19 18:04:57 +0000 2008", "favourites_count": 1427,
                                              "utc_offset": null, "time_zone": null, "geo_enabled": true,
                                              "verified": false, "statuses_count": 100008, "media_count": 26192,
                                              "lang": null, "contributors_enabled": false, "is_translator": false,
                                              "is_translation_enabled": false, "profile_background_color": "ABB8C2",
                                              "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
                                              "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
                                              "profile_background_tile": true,
                                              "profile_image_url": "http://pbs.twimg.com/profile_images/1564371419307409408/8nktWC02_normal.jpg",
                                              "profile_image_url_https": "https://pbs.twimg.com/profile_images/1564371419307409408/8nktWC02_normal.jpg",
                                              "profile_banner_url": "https://pbs.twimg.com/profile_banners/18247062/1696268589",
                                              "profile_link_color": "1B95E0", "profile_sidebar_border_color": "000000",
                                              "profile_sidebar_fill_color": "EEEEEE", "profile_text_color": "30353B",
                                              "profile_use_background_image": false, "has_extended_profile": true,
                                              "default_profile": false, "default_profile_image": false,
                                              "pinned_tweet_ids": [1767988583816651168],
                                              "pinned_tweet_ids_str": ["1767988583816651168"],
                                              "has_custom_timelines": false, "can_media_tag": true,
                                              "followed_by": false, "following": false, "follow_request_sent": false,
                                              "notifications": false, "advertiser_account_type": "promotable_user",
                                              "advertiser_account_service_levels": ["dso", "dso", "dso",
                                                                                    "media_studio"],
                                              "analytics_type": "enabled", "business_profile_state": "none",
                                              "translator_type": "none", "withheld_in_countries": [],
                                              "require_some_consent": false}}}]},
                                      "source": "<a href=\"https://studio.twitter.com\" rel=\"nofollow\">Twitter Media Studio</a>",
                                      "in_reply_to_status_id": null, "in_reply_to_status_id_str": null,
                                      "in_reply_to_user_id": null, "in_reply_to_user_id_str": null,
                                      "in_reply_to_screen_name": null,
                                      "user": {"id": 18266688, "id_str": "18266688", "name": "Tom Fitton",
                                               "screen_name": "TomFitton", "location": "Washington, DC",
                                               "description": "President, Judicial Watch. Fact checker. \"Expert\" (These are my personal views only!) LATEST BEST SELLER BOOK: A Republic Under Assault: https://t.co/0SmAJ7aAGp",
                                               "url": "https://t.co/KfcU3LJZH5", "entities": {"url": {"urls": [
                                              {"url": "https://t.co/KfcU3LJZH5",
                                               "expanded_url": "http://www.JudicialWatch.org",
                                               "display_url": "JudicialWatch.org", "indices": [0, 23]}]},
                                                                                              "description": {"urls": [{
                                                                                                                           "url": "https://t.co/0SmAJ7aAGp",
                                                                                                                           "expanded_url": "http://judicialwatchbook.com",
                                                                                                                           "display_url": "judicialwatchbook.com",
                                                                                                                           "indices": [
                                                                                                                               137,
                                                                                                                               160]}]}},
                                               "protected": false, "followers_count": 2581249,
                                               "fast_followers_count": 0, "normal_followers_count": 2581249,
                                               "friends_count": 4260, "listed_count": 6087,
                                               "created_at": "Sat Dec 20 14:32:44 +0000 2008", "favourites_count": 1955,
                                               "utc_offset": null, "time_zone": null, "geo_enabled": false,
                                               "verified": false, "statuses_count": 77802, "media_count": 8634,
                                               "lang": null, "contributors_enabled": false, "is_translator": false,
                                               "is_translation_enabled": false, "profile_background_color": "568448",
                                               "profile_background_image_url": "http://abs.twimg.com/images/themes/theme4/bg.gif",
                                               "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme4/bg.gif",
                                               "profile_background_tile": false,
                                               "profile_image_url": "http://pbs.twimg.com/profile_images/964235516794171392/ktAX5u2i_normal.jpg",
                                               "profile_image_url_https": "https://pbs.twimg.com/profile_images/964235516794171392/ktAX5u2i_normal.jpg",
                                               "profile_banner_url": "https://pbs.twimg.com/profile_banners/18266688/1527968436",
                                               "profile_link_color": "1B95E0", "profile_sidebar_border_color": "FFFFFF",
                                               "profile_sidebar_fill_color": "ECD295", "profile_text_color": "3C3940",
                                               "profile_use_background_image": false, "has_extended_profile": true,
                                               "default_profile": false, "default_profile_image": false,
                                               "pinned_tweet_ids": [1451568989050650634],
                                               "pinned_tweet_ids_str": ["1451568989050650634"],
                                               "has_custom_timelines": true, "can_media_tag": true,
                                               "followed_by": false, "following": false, "follow_request_sent": false,
                                               "notifications": false, "advertiser_account_type": "promotable_user",
                                               "advertiser_account_service_levels": ["dso", "media_studio"],
                                               "analytics_type": "enabled", "business_profile_state": "none",
                                               "translator_type": "regular", "withheld_in_countries": [],
                                               "require_some_consent": false}, "geo": null, "coordinates": null,
                                      "place": null, "contributors": null, "is_quote_status": false,
                                      "retweet_count": 1280, "favorite_count": 3092, "favorited": false,
                                      "retweeted": false, "possibly_sensitive": false,
                                      "possibly_sensitive_editable": true, "lang": "en", "supplemental_language": null},
                 "is_quote_status": false, "retweet_count": 1280, "favorite_count": 0, "favorited": false,
                 "retweeted": false, "lang": "en", "supplemental_language": null}"'''
    # 将JSON数据格式化为带缩进的字符串
    formatted_json = json.dumps(json_data, indent=4, ensure_ascii=False)
    print(formatted_json)
    return formatted_json

#获取一个F:\us-presidential文件夹下所有文件夹下的所有txt的完整路径存入input_txt_paths数组里，将input_txt_paths输出出来，并作为函数值返回
def get_txt_paths(directory):
    input_txt_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                full_path = os.path.join(root, file)
                input_txt_paths.append(full_path)

    # 输出 input_txt_paths
    for path in input_txt_paths:
        print(path)

    return input_txt_paths


# 提取并存储唯一的(screen_name, name)：
# 对于每一个 mention 对象，获取 screen_name 和 name。
# 检查 screen_name 和 name 是否存在且不为空。
def extract_screenname_and_name(input_txt_paths):
    # 输入和输出文件路径
    output_csv_path = r'F:\without_url_retweet_user_counts\screenname_and_name\screenname_and_name.csv'

    # 使用集合来存储已遇到的 (screen_name, name) 对，避免重复
    seen = set()
    for input_txt_path in input_txt_paths:
        # 打开输入文件和输出文件
        with open(input_txt_path, mode='r', encoding='utf-8') as infile, open(output_csv_path, mode='w', encoding='utf-8',
                                                                              newline='') as outfile:
            writer = csv.writer(outfile)

            # 写入CSV头
            writer.writerow(['screen_name', 'name'])

            for line in infile:
                json_data = json.loads(line.strip())  # 解析每行的 JSON 数据
                user_mentions = json_data.get('entities', {}).get('user_mentions', [])

                for mention in user_mentions:
                    screen_name = mention.get('screen_name')
                    name = mention.get('name')
                    if screen_name and name:
                        pair = (screen_name, name)
                        if pair not in seen:
                            seen.add(pair)
                            writer.writerow([screen_name, name])





def extract_screenname_and_name():
    # 输入和输出文件路径
    output_csv_path = r'F:\without_url_retweet_user_counts\screenname_and_name\screenname_and_name_id_201912_2021_02.csv'
    input_txt_paths = [r'F:\us-presidential\merge_2019_12\2019-12-01-1-merged-ok.txt', r'F:\us-presidential\merge_2020_01\2020-01-01-1-merged-ok.txt', r'F:\us-presidential\merge_2020_02\2020-02-01-1-merged-ok.txt', r'F:\us-presidential\merge_2020_03\2020-03-01-1-merged-ok.txt', r'F:\us-presidential\merge_2020_04\2020-04-01-1-merged-ok.txt', r'F:\us-presidential\merge_2020_05\2020-05-01-1-merged-ok.txt',
                       r'F:\us-presidential\merge_2020_06\2020-06-01-1-merged-ok.txt', r'F:\us-presidential\merge_2020_07\2020-07-01-1-merged-ok.txt', r'F:\us-presidential\merge_2020_08\2020-08-01-1-merged-ok.txt', r'F:\us-presidential\merge_2020_09\2020-09-01-1-merged-ok.txt',
                       r'F:\us-presidential\merge_2020_10\2020-10-01-1-merged-ok.txt', r'F:\us-presidential\merge_2020_11\2020-11-01-1-merged-ok.txt', r'F:\us-presidential\merge_2020_12\2020-12-01-1-merged-ok.txt', r'F:\us-presidential\merge_2021_01\2021-01-01-1-merged-ok.txt',
                       r'F:\us-presidential\merge_2021_02\2021-02-01-1-merged-ok.txt'
                       ]
    # 使用集合来存储已遇到的 (screen_name, name) 对，避免重复
    seen = set()
    # 打开输出文件
    with open(output_csv_path, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)

        # 写入CSV头
        writer.writerow(['screen_name', 'name', 'id_str'])

        for input_txt_path in input_txt_paths:
            print('正在处理：', input_txt_path)
            # 打开输入文件
            with open(input_txt_path, mode='r', encoding='utf-8') as infile:
                for line in infile:
                    json_data = json.loads(line.strip())  # 解析每行的 JSON 数据
                    user_mentions = json_data.get('entities', {}).get('user_mentions', [])

                    for mention in user_mentions:
                        screen_name = mention.get('screen_name')
                        name = mention.get('name')
                        id_str = mention.get('id_str')  # 获取 id_str
                        if screen_name and name and id_str:
                            pair = (screen_name, name, id_str)
                            if pair not in seen:
                                seen.add(pair)
                                writer.writerow([screen_name, name, id_str])



def drop_dupilicate():
    # 读取CSV文件
    df = pd.read_csv(r'F:\without_url_retweet_user_counts\screenname_and_name\screenname_and_name_201912_2021_02.csv')

    # 去重处理，保留第一出现的行
    df_unique = df.drop_duplicates()

    # 将结果保存到新的CSV文件
    df_unique.to_csv(r'F:\without_url_retweet_user_counts\screenname_and_name\screenname_and_name_201912_2021_02_drop_duplicate.csv', index=False)


# 补充screenname的信息
# 读取F:\without_url_retweet_user_counts\combine_without_url_retweet_user_counts.csv，csv的列名是retweet_origin_user_id,retweet_origin_username,count,screen_name。
# 其中screen_name都是空的补充上，需要从F:\without_url_retweet_user_counts\screenname_and_name\screenname_and_name_id_201912_2021_02.csv（表头是：screen_name,name,id_str）里读取id_str列的数据与第一个csv的retweet_origin_user_id进行匹配，
# 注意转换数据格式都为str进行比较，匹配上id之后就需要将第二个csv里的screen_name补充到第一个csv里
def match_screenname_according_to_userID():
    # 读取第一个CSV文件
    retweet_df = pd.read_csv('F:\\without_url_retweet_user_counts\\combine_without_url_retweet_user_counts.csv',
                             dtype={'retweet_origin_user_id': str})

    # 读取第二个CSV文件
    screenname_df = pd.read_csv(
        'F:\\without_url_retweet_user_counts\\screenname_and_name\\screenname_and_name_id_201912_2021_02.csv',
        dtype={'id_str': str})

    # 使用id_str和retweet_origin_user_id列匹配，将screen_name列合并到第一个数据框
    merged_df = retweet_df.merge(screenname_df[['id_str', 'screen_name']], how='left', left_on='retweet_origin_user_id',
                                 right_on='id_str')

    # 删除多余的id_str列
    merged_df.drop(columns=['id_str'], inplace=True)

    # 保存合并后的数据到新的CSV文件
    merged_df.to_csv('F:\\without_url_retweet_user_counts\\combined_with_screenname.csv', index=False)

# 删除掉type列的数据为Media的所有行
def delete_all_media_data():
    # 读取CSV文件
    file_path = 'F:\\code\\twitter-username-bias-type-final.csv'  # 请替换为你的CSV文件路径
    df = pd.read_csv(file_path)

    # 删除type列中值为'Media'的所有行
    df_filtered = df[df['type'] != 'Media']

    # 保存过滤后的数据到新的CSV文件
    filtered_file_path = 'F:\\code\\twitter-username-bias-type-final_without_media.csv'  # 请替换为你想保存的新的CSV文件路径
    df_filtered.to_csv(filtered_file_path, index=False)

    print("数据处理完成并已保存。")




def match_bias_according_to_screenname():
    # 读取第一个CSV文件
    retweet_df = pd.read_csv('F:\\without_url_retweet_user_counts\\combined_with_screenname.csv',
                             dtype={'screen_name': str})

    # 读取包含bias信息的第二个CSV文件
    bias_df = pd.read_csv('F:\\code\\twitter-username-bias-type-final_without_media.csv', dtype={'username': str})

    # 使用screen_name和username列匹配，将bias列合并到第一个数据框
    merged_df = retweet_df.merge(bias_df[['username', 'bias']], how='left', left_on='screen_name', right_on='username')

    # 删除多余的username列
    merged_df.drop(columns=['username'], inplace=True)

    # 保存合并后的数据到新的CSV文件
    merged_df.to_csv('F:\\without_url_retweet_user_counts\\combined_with_screenname_and_bias.csv', index=False)

#帮我统计出一个csv里有多少screen_name是空的、bias是空的、这个文件是按照count排序的，看看现在已经有bias标签的数据占count总数的多少
def count_with_bias_data_propotiton():
    # 读取CSV文件
    data_df = pd.read_csv('F:\\without_url_retweet_user_counts\\combined_with_screenname_and_bias.csv')

    # 统计screen_name和bias为空的数量
    empty_screen_name_count = data_df['screen_name'].isna().sum()
    empty_bias_count = data_df['bias'].isna().sum()

    # 按count排序
    sorted_df = data_df.sort_values(by='count', ascending=False)

    # 计算已有bias标签的数据占count总数的比例
    total_count = sorted_df['count'].sum()
    bias_count_sum = sorted_df[sorted_df['bias'].notna()]['count'].sum()
    bias_percentage = (bias_count_sum / total_count) * 100

    # 输出统计信息
    print(f"空的screen_name数量: {empty_screen_name_count}")
    print(f"空的bias数量: {empty_bias_count}")
    print(f"已有bias标签的数据占count总数的比例: {bias_percentage:.2f}%")












if __name__ == '__main__':
    # 统计所有F:\us-presidential-output\without_url文件夹下的每个月份的原帖用户id-原帖用户名-count的数据
    # months = ['2020_03','2020_04','2020_05','2020_06','2020_07','2020_08','2020_09','2020_10','2020_11','2020_12','2021_01','2021_02']
    # for month in months:
    #     # Example usage
    #     folder_path = rf'F:\us-presidential-output\without_url\output_{month}'  # Replace with your folder path
    #     # folder_path = r'F:\us-presidential-output\test'
    #     output_file = rf'F:\without_url_retweet_user_counts\{month}.csv'  # Replace with your desired output file path
    #     aggregate_retweet_counts(folder_path, output_file)



    # find_60_70_80_90_percent_data()
    # format_json()

    # # 调用函数并获取结果->提取txt里的用户的screen name和display name
    # directory_path = 'F:\\us-presidential'
    # input_txt_paths = get_txt_paths(directory_path)
    # extract_screenname_and_name(input_txt_paths)
    # extract_screenname_and_name()
    # match_screenname_according_to_userID()
    # delete_all_media_data()
    # match_bias_according_to_screenname()
    count_with_bias_data_propotiton()
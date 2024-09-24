#这是一个Python数据处理任务，
# F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\combined_with_screenname_and_bias.csv是一个映射文件，表头为retweet_origin_user_id,retweet_origin_username,count,screen_name,bias。
# 我们需要用到的是第一列、第二列和第五列。第一列和第二列的类型为string，第五列只有Right，Left和Center三种值。Right对应1，Center对应0，Left对应-1。
# 我们现在有另外一系列文件，在F:\three_parts_output\without_url下面有15个月的文件夹，它们从2019年12月到2021年2月，文件名形如output_2019_12。
# 每个文件夹里面都有若干个CSV，我们每次处理一个月内的文件。这些CSV的表头是：retweeted_time,retweeted_id,retweeted_user_id,retweeted_username,retweeted_user_location,retweeted_hashtags,retweet_time,retweet_id,retweet_expanded_urls_array,retweet_origin_user_id,retweet_origin_username,retweet_origin_user_location,retweet_origin_user_intro_expanded_url,retweet_origin_user_des_expanded_url,retweet_origin_retweet_count,retweet_origin_hashtags,quoted_time,quoted_id,quoted_expanded_urls_array,quoted_origin_user_id,quoted_origin_username,quoted_origin_user_location,quoted_origin_user_intro_expanded_url,quoted_origin_user_des_expanded_url,quoted_origin_retweet_count,quoted_origin_hashtags,retweeted_full_text,retweeted_origin_full_text,quoted_origin_full_text。
# 我们只使用其中的retweeted_user_id和retweet_origin_user_id这两列。
# 下面是我们要做的数据处理，包含两部分。
# 第一部分是，对于F:\three_parts_output\without_url下面每个月文件夹内的所有csv，我们想要统计如下数据，并生成一个表头为retweeted_user_id, retweet_times, total_bias_points, average_bias_points四列的CSV，最终得到15个CSV并写入本地。
# 对于F:\three_parts_output\without_url下面一个月文件夹内的所有csv中的数据，如果retweet_origin_user_id在F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\combined_with_screenname_and_bias.csv中出现，那么就将对应的bias的映射值（-1 0或者1）加到retweeted_user_id对应的total_bias_points上，同时为retweet_times加1。
# 最终对于每个月的所有retweeted_user_id，用total_bias_points除以retweet_times得到average_bias_points。
#
# 以下是第二部分的数据处理，请注意，不同于第一部分我们独立处理每个月的数据（并最终得到15个月的csv），第二部分中，我们跨15个月进行处理。我们希望最终得到一个csv，表头为retweet_origin_user_id和total_times。
# 对于F:\three_parts_output\without_url下面十五个月文件夹内的所有csv，如果retweet_origin_user_id在F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\combined_with_screenname_and_bias.csv中排前十，那么我们就对相应的total_times加1。
# 换言之，我们在统计F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\combined_with_screenname_and_bias.csv中排名前十名的retweet_origin_user_id每个究竟出现了多少次。


import os
import pandas as pd

# Path to the mapping file
mapping_file_path = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\combined_with_screenname_and_bias.csv'

# Load the mapping file
mapping_df = pd.read_csv(mapping_file_path, usecols=['retweet_origin_user_id', 'bias'])

# Convert bias values
bias_map = {'Right': 1, 'Center': 0, 'Left': -1}
mapping_df['bias'] = mapping_df['bias'].map(bias_map)

# Top 10 retweet_origin_user_id based on counts in mapping file
top_10_ids = mapping_df['retweet_origin_user_id'].value_counts().head(10).index

# Monthly processing for Part 1
monthly_dir = r'F:\three_parts_output\single_url\twitter_url'
for month in os.listdir(monthly_dir):
    month_path = os.path.join(monthly_dir, month)

    # Initialize a dictionary to store results for the month
    results = {}

    # Process each file in the month directory
    for file_name in os.listdir(month_path):
        file_path = os.path.join(month_path, file_name)
        df = pd.read_csv(file_path, usecols=['retweeted_user_id', 'retweet_origin_user_id'])

        # Iterate through rows and update results
        for _, row in df.iterrows():
            retweeted_user_id = row['retweeted_user_id']
            retweet_origin_user_id = row['retweet_origin_user_id']

            if retweet_origin_user_id in mapping_df['retweet_origin_user_id'].values:
                bias_value = \
                mapping_df.loc[mapping_df['retweet_origin_user_id'] == retweet_origin_user_id, 'bias'].values[0]

                if retweeted_user_id not in results:
                    results[retweeted_user_id] = {'retweet_times': 0, 'total_bias_points': 0}

                results[retweeted_user_id]['retweet_times'] += 1
                results[retweeted_user_id]['total_bias_points'] += bias_value

    # Calculate average bias points
    for user_id in results:
        results[user_id]['average_bias_points'] = results[user_id]['total_bias_points'] / results[user_id][
            'retweet_times']

    # Convert results to DataFrame and save to CSV
    output_df = pd.DataFrame.from_dict(results, orient='index').reset_index()
    output_df.columns = ['retweeted_user_id', 'retweet_times', 'total_bias_points', 'average_bias_points']
    output_file_path = os.path.join(monthly_dir, f'{month}_processed.csv')
    output_df.to_csv(output_file_path, index=False)

# Cross-month processing for Part 2
cross_month_results = {user_id: 0 for user_id in top_10_ids}

for month in os.listdir(monthly_dir):
    month_path = os.path.join(monthly_dir, month)

    for file_name in os.listdir(month_path):
        file_path = os.path.join(month_path, file_name)
        df = pd.read_csv(file_path, usecols=['retweet_origin_user_id'])

        # Count appearances of top 10 IDs
        for retweet_origin_user_id in df['retweet_origin_user_id']:
            if retweet_origin_user_id in cross_month_results:
                cross_month_results[retweet_origin_user_id] += 1

# Save cross-month results to CSV
cross_month_df = pd.DataFrame(list(cross_month_results.items()), columns=['retweet_origin_user_id', 'total_times'])
cross_month_df.to_csv(r'F:\three_parts_output\cross_month_results3.csv', index=False)


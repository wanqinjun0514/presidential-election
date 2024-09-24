import os
import pandas as pd
from collections import defaultdict

# Path to the mapping file
mapping_file_path = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\1_without_url_retweet_user_counts\combined_with_screenname_and_bias.csv'

# Load the mapping file, considering only the first and fifth columns
mapping_df = pd.read_csv(mapping_file_path, usecols=['retweet_origin_user_id', 'bias'], dtype='str')

# Convert bias values to numerical
bias_map = {'Right': 1, 'Center': 0, 'Left': -1}
mapping_df['bias'] = mapping_df['bias'].map(bias_map)

# Determine the top 10 rows based on criteria (e.g., highest bias values or another metric)
top_10_df = mapping_df.head(10)
top_10_ids = top_10_df['retweet_origin_user_id'].tolist()

# Directory containing the 15 months of data
monthly_dir = r'F:\three_parts_output\single_url\twitter_url'
res_dir = r'F:\Intermediate Results\top10\twitter_url'

# Process each month's folder
for month in os.listdir(monthly_dir):
    print(month)
    month_path = os.path.join(monthly_dir, month)

    # Dictionary to store retweeted_user_id and associated retweet_origin_user_id with counts
    associations = defaultdict(lambda: defaultdict(int))

    # Process each CSV file in the month's folder
    for file_name in os.listdir(month_path):
        print(file_name)
        file_path = os.path.join(month_path, file_name)
        df = pd.read_csv(file_path, usecols=['retweeted_user_id', 'retweet_origin_user_id'], dtype=str)

        # Iterate through each row in the CSV
        for _, row in df.iterrows():
            retweeted_user_id = row['retweeted_user_id']
            retweet_origin_user_id = row['retweet_origin_user_id']

            # Check if retweet_origin_user_id is in the top 10
            if retweet_origin_user_id in top_10_ids:
                associations[retweeted_user_id][retweet_origin_user_id] += 1

    # Prepare the output data
    output_data = []
    for user_id, origin_dict in associations.items():
        for origin_id, count in origin_dict.items():
            output_data.append([user_id, origin_id, count])

    # Create a DataFrame for the output data
    output_df = pd.DataFrame(output_data, columns=['retweeted_user_id', 'associated_retweet_origin_user_id', 'count'])

    # Save the result as a CSV file
    output_file_path = os.path.join(res_dir, f'{month}_top_10_associations_with_counts.csv')
    output_df.to_csv(output_file_path, index=False)

print("Processing complete.")
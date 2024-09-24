import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 政客对三个部分数据的意识形态画分布图
# 三个部分的数据政客对用户的打分结果在F:\Experimental Results\Average_Bias_Rating\politician_average_rating\twitter_url-rating（其他两个部分也都在politician_average_rating下面），里面的结果是每个月一个用户打分结果的csv，表头是retweeted_user_id,total_bias_points,retweet_times,average_bias_points，根据average_bias_points字段从-1到1区间里每隔0.1划分一次小区间，统计每个月份结果里的每个小区间里有多少个用户，画一个图
def politician_to_three_parts_data_user_bias_distribution_plot():
    # Define the directories
    # input_dir = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\twitter_url-rating'
    # input_dir = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\2_monthly_users_bias'
    input_dir = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\external_url-rating'

    # twitter_url部分的输出路径
    # output_data_dir = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\twitter_url-rating\pic_twitter_url-rating_divided_by_0.1\data'
    # output_pic_dir = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\twitter_url-rating\pic_twitter_url-rating_divided_by_0.1\pic'
    # without_url部分的输出路径
    # output_data_dir = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\pic_without_url-rating_divided_by_0.1\data'
    # output_pic_dir = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\without_url-rating\pic_without_url-rating_divided_by_0.1\pic'
    # external_url部分的输出路径
    output_data_dir = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\external_url-rating\pic_external_url-rating_divided_by_0.1\data'
    output_pic_dir = r'F:\Experimental Results\Average_Bias_Rating\politician_average_rating\external_url-rating\pic_external_url-rating_divided_by_0.1\pic'

    # Ensure the output directories exist
    os.makedirs(output_data_dir, exist_ok=True)
    os.makedirs(output_pic_dir, exist_ok=True)

    # Define the bins for average_bias_points, including 1 in the last interval
    bins = np.arange(-1, 1.1, 0.1)
    bins[-1] = 1.01  # Extend the last bin to include 1 exactly
    labels = [f'{round(bins[i], 1)} to {round(bins[i + 1], 1)}' for i in range(len(bins) - 1)]

    # Process each month's data
    for file in os.listdir(input_dir):
        if file.endswith('_output.csv'):
            # Load the CSV file
            file_path = os.path.join(input_dir, file)
            df = pd.read_csv(file_path)

            # Bin the data based on average_bias_points
            df['bias_interval'] = pd.cut(df['average_bias_points'], bins=bins, labels=labels, include_lowest=True,
                                         right=False)

            # Count the number of users in each interval
            interval_counts = df['bias_interval'].value_counts().sort_index()

            # Save the interval counts to a CSV file
            output_data_file = os.path.join(output_data_dir, f'{file[:-4]}_interval_counts.csv')
            interval_counts.to_csv(output_data_file, header=['count'])

            # Plot the distribution as a bar graph
            plt.figure(figsize=(10, 6))
            interval_counts.plot(kind='bar', color='skyblue')
            plt.title(f'User Distribution by Bias Interval ({file[:-4]})')
            plt.xlabel('Bias Interval')
            plt.ylabel('Number of Users')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # Save the plot as an image
            output_pic_file = os.path.join(output_pic_dir, f'{file[:-4]}_distribution.png')
            plt.savefig(output_pic_file)
            plt.close()

            # Print the number of users processed
            num_users = len(df)
            print(f'Processed {num_users} users for {file[:-4]}')

    print("Processing completed.")




def media_to_three_parts_data_user_bias_distribution_plot():
    # input_dir = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\twitter_url-rating'
    # output_data_dir = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\twitter_url-rating\pic_twitter_url-rating_divided_by_0.1\data'
    # output_pic_dir = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\twitter_url-rating\pic_twitter_url-rating_divided_by_0.1\pic'
    # input_dir = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\without_url-rating'
    # output_data_dir = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\without_url-rating\pic_twitter_url-rating_divided_by_0.1\data'
    # output_pic_dir = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\without_url-rating\pic_twitter_url-rating_divided_by_0.1\pic'
    # input_dir = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating'
    # output_data_dir = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating\pic_twitter_url-rating_divided_by_0.1\data'
    # output_pic_dir = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\external_url-rating\pic_twitter_url-rating_divided_by_0.1\pic'
    input_dir = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\multiple_url-rating'
    output_data_dir = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\multiple_url-rating\pic_twitter_url-rating_divided_by_0.1\data'
    output_pic_dir = r'F:\Experimental Results\Average_Bias_Rating\media_average_rating\multiple_url-rating\pic_twitter_url-rating_divided_by_0.1\pic'
    # Ensure the output directories exist
    os.makedirs(output_data_dir, exist_ok=True)
    os.makedirs(output_pic_dir, exist_ok=True)

    # Define the bins for average_bias_points, including 1 in the last interval
    bins = np.arange(-2, 2.1, 0.1)
    # bins[-1] = 1.01  # Extend the last bin to include 1 exactly
    labels = [f'{round(bins[i], 1)} to {round(bins[i + 1], 1)}' for i in range(len(bins) - 1)]

    # Process each month's data
    for file in os.listdir(input_dir):
        if file.endswith('.csv'):
            # Load the CSV file
            file_path = os.path.join(input_dir, file)
            df = pd.read_csv(file_path)
            print(file_path)

            # Bin the data based on average_bias_points
            df['bias_interval'] = pd.cut(df['average_bias_points'], bins=bins, labels=labels, include_lowest=True,
                                         right=False)

            # Count the number of users in each interval
            interval_counts = df['bias_interval'].value_counts().sort_index()

            # Save the interval counts to a CSV file
            output_data_file = os.path.join(output_data_dir, f'{file[:-4]}_interval_counts.csv')
            interval_counts.to_csv(output_data_file, header=['count'])

            # Plot the distribution as a bar graph
            plt.figure(figsize=(10, 6))
            interval_counts.plot(kind='bar', color='skyblue')
            plt.title(f'User Distribution by Bias Interval ({file[:-4]})')
            plt.xlabel('Bias Interval')
            plt.ylabel('Number of Users')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # Save the plot as an image
            output_pic_file = os.path.join(output_pic_dir, f'{file[:-4]}_distribution.png')
            plt.savefig(output_pic_file)
            plt.close()

            # Print the number of users processed
            num_users = len(df)
            print(f'Processed {num_users} users for {file[:-4]}')

    print("Processing completed.")



if __name__ == '__main__':
    media_to_three_parts_data_user_bias_distribution_plot()
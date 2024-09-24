def dataDistributionCheck(A): 
    # 计算每一行和每一列的和
    row_sums = np.sum(A, axis=1)  # 每一行的和（用户转发行为）
    col_sums = np.sum(A, axis=0)  # 每一列的和（政客被转发次数）

    # 创建数据框
    row_sums_df = pd.DataFrame({'User num': range(len(row_sums)), 'Total_Retweets': row_sums})
    col_sums_df = pd.DataFrame({'Influencer num': range(len(col_sums)), 'Total_Retweets': col_sums})

    # 保存为CSV文件
    row_sums_df.to_csv('data/test/row_sums.csv', index=False)
    col_sums_df.to_csv('data/test/col_sums.csv', index=False)
    print("row_sums 和 col_sums 已保存为CSV文件")

    # 绘制用户转发行为的分布图
    plt.figure(figsize=(10, 6))
    plt.hist(row_sums, bins=100, color='green', alpha=0.7)
    plt.title('User Total Retweets Distribution')
    plt.xlabel('Total Retweets per User')
    plt.ylabel('Number of Users')
    plt.show()

    # 绘制政客被转发行为的分布图
    plt.figure(figsize=(10, 6))
    plt.hist(col_sums, bins=100, color='blue', alpha=0.7)
    plt.title('Influencer Total Retweets Distribution')
    plt.xlabel('Total Retweets per Influencer')
    plt.ylabel('Number of Influencers')
    plt.show()


def userActivityCheck(A):
    # 统计每个用户转发的政客数（每行非零值的个数）
    user_activity = np.count_nonzero(A, axis=1)

    # 统计每个政客被转发的用户数（每列非零值的个数）
    influencer_activity = np.count_nonzero(A, axis=0)

    # 绘制用户活跃度的分布
    plt.figure(figsize=(10, 6))
    plt.hist(user_activity, bins=100, color='green', alpha=0.7)
    plt.title('User Activity Distribution')
    plt.xlabel('Number of Influencers Each User Retweeted')
    plt.ylabel('Number of Users')
    plt.show()

    # 绘制政客被转发次数的分布
    plt.figure(figsize=(10, 6))
    plt.hist(influencer_activity, bins=100, color='blue', alpha=0.7)
    plt.title('Influencer Activity Distribution')
    plt.xlabel('Number of Users Retweeting Each Influencer')
    plt.ylabel('Number of Influencers')
    plt.show()


def check_singular_matrix(matrix):
    condition_number = np.linalg.cond(matrix)
    print(f"The condition number of the matrix is {condition_number}")

    if condition_number > 1e10:
        print("The matrix is likely to be singular.")
    else:
        print("The matrix is not singular.")


def debug(filepath):
    global deleted_rows, deleted_cols
    A = create_adjacency_matrix(filepath)
    print(A.shape)
    A, deleted_rows, deleted_cols = matrixOptimization(A, 3)
    print(A.shape)
    dataDistributionCheck(A)
    userActivityCheck(A)
    check_singular_matrix(A)
    P = normalize_matrix(A)
    num_zero_rows, num_zero_columns = count_zero_rows_and_columns(P)
    print(type(P[1][1]))
    print(f'P共有{num_zero_rows}个全0行及{num_zero_columns}个全0列')
    S = calculate_residuals(P)
    print('residuals calculate success')
    print(S.shape)
    check_matrix_validity(S)
    print(type(S[1][1]))

    num_zero_rows, num_zero_columns = count_zero_rows_and_columns(S)
    print(f'S共有{num_zero_rows}个全0行及{num_zero_columns}个全0列')

    U0, Sigma, V = perform_svd(S)

    # 打印奇异值
    print(f"奇异值的前几个值: {Sigma[:10]}")

    # 绘制奇异值的分布图
    plt.figure(figsize=(10, 6))
    plt.plot(Sigma, marker='o')
    plt.title('Singular Values Distribution')
    plt.xlabel('Index')
    plt.ylabel('Singular Value')
    plt.yscale('log')  # 采用对数坐标
    plt.show()
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

deleted_rows = []
deleted_cols = []
Users = []
Influencers = []


#矩阵优化——删除不活跃用户数据并标记删除的行和列
# 代码的功能是优化一个矩阵，通过删除不活跃用户的数据，并标记被删除的行和列。具体步骤如下：
# 计算行的和：计算矩阵每一行的总和。
# 标记行：根据一个基准值（benchmark），标记出总和低于该值的行。
# 删除行：删除不活跃的行，得到新的矩阵。
# 计算列的和：对新矩阵计算每一列的总和。
# 标记列：标记出和为零的列。
# 删除列：删除这些和为零的列。
# 最终返回优化后的矩阵，以及被删除的行和列的索引。
def matrixOptimization(matrix, benchmark):
    # 计算每一行的和
    row_sums = np.sum(matrix, axis=1)
    # 标记哪些行被删除
    rows_to_keep = row_sums > benchmark
    print(rows_to_keep)
    deleted_rows = np.where(~rows_to_keep)[0]  # 记录被删除的行
    # 删除行和小于 benchmark 的行
    matrix = matrix[rows_to_keep, :]
    # 计算每一列的和
    col_sums = np.sum(matrix, axis=0)
    # 标记哪些列被删除
    cols_to_keep = col_sums > 0
    deleted_cols = np.where(~cols_to_keep)[0]  # 记录被删除的列

    # 删除列和为0的列
    matrix = matrix[:, cols_to_keep]
    return matrix, deleted_rows, deleted_cols



#统计用户转发情况。
def forwardingCount(A):
    row_sums = np.sum(A, axis=1)
    # 统计相同行和出现的次数
    sum_counts = Counter(row_sums)
    print("矩阵的每一行的和：", row_sums)
    print("用户转发次数统计：", sum_counts)


# 读取一个月的转发数据，构成转发矩阵
def create_adjacency_matrix(filepath):
    # 加载CSV文件
    allUsers = np.array([])
    Urls = np.array([])
    df = pd.read_csv(filepath, dtype=str, usecols=['retweeted_user_id', 'retweet_origin_screenname'])
    tmpusers = df['retweeted_user_id'].unique()
    tmpurls = df['retweet_origin_screenname'].unique()
    # print(type(tmpusers))
    # print(type(tmpurls))
    allUsers = np.unique(np.concatenate((allUsers, tmpusers)))
    Urls = np.unique(np.concatenate((Urls, tmpurls)))
    # print('allUser num', len(allUsers))
    # users = allUsers[:5000]
    users = allUsers
    # print(len(allUsers))
    # print(len(users), users)
    # print(len(Urls), Urls)
    userindex, urlindex = {}, {}

    # 转发矩阵每行对应用户
    global Users, Influencers
    Users = users
    Influencers = Urls

    for i in range(len(users)):
        user = users[i]
        if user in userindex:
            print('Problem!')
        else:
            userindex[user] = i
    for i in range(len(Urls)):
        url = Urls[i]
        if url in urlindex:
            print('Problem!')
        else:
            urlindex[url] = i
    A = np.zeros((len(users), len(Urls)), dtype=int)

    # 填充转发矩阵
    df = pd.read_csv(filepath, dtype=str, usecols=['retweeted_user_id', 'retweet_origin_screenname'])
    for i in tqdm(range(len(df)), desc='Processing matrix'):
        user = df['retweeted_user_id']
        url = df['retweet_origin_screenname']
        if user[i] not in userindex:
            continue
        # print(userindex[user[i]], domainindex[domain[i]])
        A[userindex[user[i]]][urlindex[url[i]]] += 1.0
        # print('check')
    return A


# 生成标准化矩阵
def normalize_matrix(A):
    total_retweets = np.sum(A)
    P = A / total_retweets
    return P


# 计算残差矩阵
def calculate_residuals(P):
    r = np.sum(P, axis=1)
    c = np.sum(P, axis=0)
    # print(len(r), len(c))
    rc = np.outer(r, c)
    # P-rc:用户具体转发频率-用户习惯与媒体影响力耦合结果 => 反应用户对媒体的倾向程度
    tmp = rowmul(r, P-rc)
    S = colmul(c, tmp)
    # S = np.linalg.inv(np.sqrt(D_r)) @ (P - rc) @ np.linalg.inv(np.sqrt(D_c))
    return S

# 对矩阵 A 的每一行进行归一化处理
def rowmul(r, A):
    matShape = A.shape
    mat = np.zeros(matShape, dtype=float)
    for i in range(len(r)):
        scalar = r[i]
        mat[i, :] = A[i, :] / np.sqrt(scalar)
    return mat


def colmul(c, A):
    matShape = A.shape
    mat = np.zeros(matShape, dtype=float)
    for j in range(len(c)):
        scalar = c[j]
        mat[:, j] = A[:, j] / np.sqrt(scalar)
    return mat


def perform_svd(S):
    # Step 1: 计算 S^T S
    STS = np.dot(S.T, S)

    # Step 2: 对 S^T S 进行特征值分解
    eigenvalues, V = np.linalg.eig(STS)

    # Step 3: 对特征值进行排序
    idx = np.argsort(eigenvalues)[::-1]  # 降序排序
    eigenvalues = eigenvalues[idx]
    V = V[:, idx]

    # Step 4: 计算奇异值矩阵 Sigma
    sigma = np.sqrt(eigenvalues)

    # Step 5: 计算 U 矩阵第一列

    Sigma_inv = np.diag(1 / sigma)
    U0 = np.dot(S, V[:, 0].reshape(-1, 1)) * Sigma_inv[0, 0]
    return U0






def perform_svd_错的(S):
    # Step 1: 计算 S^T S
    STS = np.dot(S.T, S)

    # Step 2: 对 S^T S 进行特征值分解
    eigenvalues, V = np.linalg.eig(STS)
    # print(V)
    # print(f'eigvalues:{eigenvalues}')
    idx = np.argsort(eigenvalues)[::-1]  # 降序排序
    eigenvalues = eigenvalues[idx]
    print(f'eigvalues:{eigenvalues}')

    # Step 3: 计算奇异值矩阵 Sigma
    try:
        sigma = np.sqrt(eigenvalues)
    except RuntimeWarning:
        print(f'eigvalues:{eigenvalues}')
        return
    print(f'sigma{sigma}')
    Sigma = np.diag(sigma)

    # Step 4: 计算 U 的第一列
    Sigma_inv = np.diag(1 / sigma)
    U0 = np.dot(S, V[:, 0].reshape(-1, 1)) * Sigma_inv[0, 0]

    return U0, Sigma, V


def infer_user_positions(U0, r):
    # 用户位置由标准化的第一个主成分决定
    user_positions = rowmul(r, U0)
    # 标准化用户位置
    user_positions_standardized = (user_positions - np.mean(user_positions)) / np.std(user_positions)
    return user_positions_standardized


def infer_influencer_positions(A, user_positions):
    # 影响者位置由其转推者的位置中位数决定
    influencer_positions = []
    for j in range(A.shape[1]):
        # 获取影响者j的所有转推者位置
        retweeters = A[:, j] > 0
        positions = user_positions[retweeters]
        if positions.size > 0:
            # 计算中位数
            median_position = np.median(positions)
            influencer_positions.append(median_position)
        else:
            influencer_positions.append(np.nan)  # 如果没有转推者，则返回NaN
    return influencer_positions


def graph_user_position(data_users, title, xlabel, ylabel, filename):
    plt.figure(figsize=(10, 6))

    # 使用seaborn绘制KDE密度图
    bins = np.linspace(-2, 2, 100)
    sns.histplot(data_users, bins=bins, color='green', alpha=0.5, kde=True, label='users')
    # sns.histplot(data_influencers, bins=100, color='purple', alpha=0.5, kde=True, label='influencers')

    # 设置图表属性
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlim(-2, 2)
    plt.legend()
    plt.savefig(filename)
    plt.show()


def graph_influencer_position(data_influencers, title, xlabel, ylabel, filename):
    plt.figure(figsize=(10, 6))

    # 使用seaborn绘制KDE密度图
    bins = np.linspace(-2, 2, 100)
    # sns.histplot(data_users, bins=100, color='green', alpha=0.5, kde=True, label='users')
    sns.histplot(data_influencers, bins=bins, color='purple', alpha=0.5, kde=True, label='influencers')

    # 设置图表属性
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlim(-2, 2)
    plt.legend()
    plt.savefig(filename)
    plt.show()


def check_matrix_validity(matrix):
    if np.any(np.isnan(matrix)):
        print("Matrix contains NaN values")
    if np.any(np.isinf(matrix)):
        print("Matrix contains Inf values")


def count_zero_rows_and_columns(matrix):
    # 计算全零的行数
    zero_rows = np.sum(matrix, axis=1) == 0
    num_zero_rows = np.sum(zero_rows)
    # 计算全零的列数
    zero_columns = np.sum(matrix, axis=0) == 0
    num_zero_columns = np.sum(zero_columns)
    return num_zero_rows, num_zero_columns


def dataDistributionCheck(A):
    # 计算每一行和每一列的和
    row_sums = np.sum(A, axis=1)  # 每一行的和（用户转发行为）
    col_sums = np.sum(A, axis=0)  # 每一列的和（政客被转发次数）

    # 创建数据框
    row_sums_df = pd.DataFrame({'User num': range(len(row_sums)), 'Total_Retweets': row_sums})
    col_sums_df = pd.DataFrame({'Influencer num': range(len(col_sums)), 'Total_Retweets': col_sums})

    # 保存为CSV文件
    # row_sums_df.to_csv('data/test/row_sums.csv', index=False)
    # col_sums_df.to_csv('data/test/col_sums.csv', index=False)
    # print("row_sums 和 col_sums 已保存为CSV文件")

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
    A, deleted_rows, deleted_cols = matrixOptimization(A, 4)# 在此处修改需要筛选的转发次数
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


def calculate_positions(filepath):
    global deleted_rows, deleted_cols
    A = create_adjacency_matrix(filepath)
    print(A.shape)
    A, deleted_rows, deleted_cols = matrixOptimization(A, 1)

    print(A.shape)

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

    U0 = perform_svd(S)

    print('------------------------------------------------------')
    print('U0:',U0)
    print(U0.shape)
    print('------------------------------------------------------')

    if U0[0] > 0:
        U0 = -U0
    r = np.sum(P, axis=1)
    print("r0:",r)
    print(r.shape)
    #log_r = np.log(r )
    #log_U0 = np.log(np.abs(U0))  # 对U0取绝对值，避免对负数取对数
    print("sqrt(r)",np.sqrt(r))
    #user_positions = np.exp(log_U0 - 0.5 * log_r)
    #user_positions = U0 / np.sqrt(r)
    user_positions = infer_user_positions(U0, r)
    print("user_positions:",user_positions)
    print(user_positions.shape)
    user_positions_standardized = user_positions
    print("user_positions_standardized:", user_positions_standardized)
    print(user_positions_standardized.shape)
    influencer_positions = infer_influencer_positions(A, user_positions)

    # print(f'奇异值分解结果:\n{U0}\n{sigma}\n{V}')
    print("User Positions (Standardized):\n", user_positions)
    print("Influencer Positions (Median of Retweeter Positions):\n", influencer_positions)
    print(f'check: {len(user_positions)} = {len(Users)} - {len(deleted_rows)} = {len(Users) - len(deleted_rows)}')
    print(f'check: {len(influencer_positions)} = {len(Influencers)} - {len(deleted_cols)} = {len(Influencers) - len(deleted_cols)}')
    return user_positions, influencer_positions


def save_scores_to_csv(user_positions, influencer_positions, output_user_csv, output_influencer_csv):
    global Users, Influencers, deleted_cols, deleted_rows
    user_positions = np.ravel(user_positions)
    influencer_positions = np.ravel(influencer_positions)

    # 筛选保留的用户和政客
    kept_users = np.delete(Users, deleted_rows)
    kept_influencers = np.delete(Influencers, deleted_cols)

    # 将用户ID与对应的用户分数合并
    user_data = {
        'UserID': kept_users,
        'UserScore': user_positions
    }
    user_df = pd.DataFrame(user_data)

    # 将政客ID与对应的政客分数合并
    influencer_data = {
        'InfluencerID': kept_influencers,
        'InfluencerScore': influencer_positions
    }
    influencer_df = pd.DataFrame(influencer_data)

    # 保存为CSV文件
    user_df.to_csv(output_user_csv, index=False)
    influencer_df.to_csv(output_influencer_csv, index=False)

    print(f"User scores saved to {output_user_csv}")
    print(f"Influencer scores saved to {output_influencer_csv}")


def main():
    directory = rf'F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Politician\twitter_url'
    for i in range(2020, 2022):
        year = str(i)
        for j in range(1, 13):
            if j < 12 and i == 2019:
                continue
            if j > 2 and i == 2021:
                continue
            month = str(j).zfill(2)
            filename = f'politician_influence_Simplyfied_Forwarding_output_{year}_{month}.csv'
            # print(filename)
            filepath = os.path.join(directory, filename)
            print(filepath)
            # debug(filepath)
            user_positions, influencer_positions = calculate_positions(filepath)
            graph_user_position(user_positions, 'Bias', 'Score', 'number',
                                rf"F:\Experimental Results\Matrix Decomposition Results\politician_results\twitter_url_politicians_and_users_bias_results_graph\{filename.split('.')[0]}_user.png")
            graph_influencer_position(influencer_positions, 'Bias', 'Score', 'number',
                                      rf"F:\Experimental Results\Matrix Decomposition Results\politician_results\twitter_url_politicians_and_users_bias_results_graph\{filename.split('.')[0]}_influencer.png")
            save_scores_to_csv(user_positions, influencer_positions,
                               rf"F:\Intermediate Results\Matrix Decomposition Results\politician_results\twitter_url\{filename.split('.')[0]}_user.csv",
                               rf"F:\Intermediate Results\Matrix Decomposition Results\politician_results\twitter_url\{filename.split('.')[0]}_influencer.csv")




if __name__ == "__main__":
    main()
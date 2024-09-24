import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
# 这段代码的核心是通过奇异值分解（SVD）对媒体和普通用户的政治倾向分数进行分解，具体过程如下：
#
# 数据准备与矩阵构建：
#
# create_adjacency_matrix() 函数通过读取CSV文件，构建用户与媒体之间的转发矩阵，矩阵中的每个元素代表某个用户转发某个媒体的次数。行表示用户，列表示媒体或影响者。
# 矩阵优化：
#
# matrixOptimization() 函数通过删除不活跃的用户和无效的媒体（如那些几乎没有被转发或没有转发内容的），对转发矩阵进行优化，减少计算量。
# 标准化矩阵：
#
# normalize_matrix() 函数对矩阵进行标准化处理，将转发次数除以总转发次数，得到一个概率矩阵，表示每个用户与媒体的相对关联强度。
# 计算残差矩阵：
#
# calculate_residuals() 函数用于计算残差矩阵。残差矩阵反映了用户转发频率与用户习惯和媒体影响力的差异，通过行与列的乘积减去每个用户与媒体的耦合结果。这样，残差矩阵能够揭示出用户对特定媒体的偏好程度。
# 奇异值分解（SVD）：
#
# perform_svd() 函数执行SVD分解，将残差矩阵分解为用户和媒体的特征向量及其对应的奇异值矩阵。这些奇异值代表了用户和媒体在不同维度上的相对重要性。第一个特征向量用于估计用户和媒体的政治倾向位置。
# 用户与媒体倾向计算：
#
# infer_user_positions() 函数利用第一个特征向量推断用户的政治倾向分数。用户的位置由标准化的第一个主成分决定。
# infer_influencer_positions() 函数根据媒体的所有转发者的位置中位数来确定每个媒体的政治倾向。
# 结果保存与可视化：
#
# 用户和媒体的政治倾向分数会通过 save_scores_to_csv() 保存为CSV文件，方便后续的分析。
# graph_user_position() 和 graph_influencer_position() 函数通过绘制分布图来展示用户和媒体的倾向分布情况。
# 整体流程总结：
# 代码通过分析用户转发媒体的行为数据，构建用户-媒体矩阵。
# 然后通过矩阵优化删除不活跃用户和无效媒体，并标准化转发矩阵。
# 通过残差矩阵计算，揭示用户对不同媒体的具体偏好。
# 最后，通过奇异值分解提取出用户和媒体的政治倾向，并通过可视化和保存结果，完成对用户和媒体政治倾向的分解与分析。
# 这一方法主要利用了SVD对高维矩阵的降维特性，通过用户的转发行为，推断出其对不同媒体的政治倾向。

deleted_rows = []
deleted_cols = []
Users = []
Influencers = []


#矩阵优化——删除不活跃用户数据并标记删除的行和列
def matrixOptimization(matrix, benchmark):
    # 计算每一行的和
    row_sums = np.sum(matrix, axis=1)
    # 标记哪些行被删除
    rows_to_keep = row_sums > benchmark
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


def check_singular_matrix(matrix):
    condition_number = np.linalg.cond(matrix)
    print(f"The condition number of the matrix is {condition_number}")

    if condition_number > 1e10:
        print("The matrix is likely to be singular.")
    else:
        print("The matrix is not singular.")


# 读取一个月的转发数据，构成转发矩阵
def create_adjacency_matrix(filepath):
    # 加载CSV文件
    allUsers = np.array([])
    Urls = np.array([])
    df = pd.read_csv(filepath, dtype=str, usecols=['retweeted_user_id', 'matched_domain'])
    tmpusers = df['retweeted_user_id'].unique()
    tmpurls = df['matched_domain'].unique()
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
    df = pd.read_csv(filepath, dtype=str, usecols=['retweeted_user_id', 'matched_domain'])
    for i in tqdm(range(len(df)), desc='Processing matrix'):
        user = df['retweeted_user_id']
        url = df['matched_domain']
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
    # print(V)
    # print(f'eigvalues:{eigenvalues}')
    idx = np.argsort(eigenvalues)[::-1]  # 降序排序
    eigenvalues = eigenvalues[idx]
    # print(f'eigvalues:{eigenvalues}')

    # Step 3: 计算奇异值矩阵 Sigma
    sigma = np.sqrt(eigenvalues)
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


def calculate_positions(filepath):
    global deleted_rows, deleted_cols
    A = create_adjacency_matrix(filepath)
    print(A.shape)
    A, deleted_rows, deleted_cols = matrixOptimization(A, 5)
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

    U0, sigma, V = perform_svd(S)
    if U0[0][0] > 0:
        U0 = -U0
    r = np.sum(P, axis=1)
    user_positions = infer_user_positions(U0, r)
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
    # directory = r'F:\Intermediate Results\Simplyfied Forwarding relationship\test_Simplyfied Forwarding relationship_Media'# 先测试
    directory = r'F:\Intermediate Results\Simplyfied Forwarding relationship\Simplyfied Forwarding relationship_Media'

    for i in range(2019, 2022):
        year = str(i)
        for j in range(1, 13):
            if j < 12 and i == 2019:
                continue
            if j > 2 and i == 2021:
                continue
            month = str(j).zfill(2)
            filename = f'output_{year}_{month}.csv'
            # print(filename)
            filepath = os.path.join(directory, filename)
            print(filepath)
            # calculate_positions(filepath, year, month)
            user_positions, influencer_positions = calculate_positions(filepath)
            graph_user_position(user_positions, 'Bias', 'Score', 'number', f"F:/Experimental Results/Matrix Decomposition Results/medias_and_users_bias_results_graph_all_retweet_data/{filename.split('.')[0]}_user.png")
            graph_influencer_position(influencer_positions, 'Bias', 'Score', 'number', f"F:/Experimental Results/Matrix Decomposition Results/medias_and_users_bias_results_graph_all_retweet_data/{filename.split('.')[0]}_influencer.png")
            save_scores_to_csv(user_positions, influencer_positions, f"F:/Intermediate Results/Matrix Decomposition Results/media_results/{filename.split('.')[0]}_user.csv", f"F:/Intermediate Results/Matrix Decomposition Results/media_results/{filename.split('.')[0]}_influencer.csv")
            # return


if __name__ == "__main__":
    main()

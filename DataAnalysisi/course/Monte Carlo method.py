# PI=概率*4
import matplotlib.pyplot as plt
import random
import math
#
# n1 = 1000000
# n2 = 0
#
# for i in range(n1):
#     x = random.random()
#     y = random.random()
#
#     dis = (x**2 + y**2)**0.5
#
#     if dis <= 1:
#         n2 += 1
#
# print("PI is ", 4 * n2/n1)

def monte_carlo_pi(max_trials, record_interval):
    total = 0
    in_count = 0
    errors = []
    trials = []

    for i in range(1, max_trials + 1):
        x = random.random()
        y = random.random()
        dis = (x**2 + y**2)**0.5
        if dis <= 1:
            in_count += 1
        total += 1
        if i % record_interval == 0:  # 每隔record_interval次记录一次
            pi_estimate = 4 * in_count / total
            error = abs(pi_estimate - math.pi) / math.pi
            errors.append(error)
            trials.append(i)

    return trials, errors

def find_min_trials_for_alpha(alpha):
    total = 0
    in_count = 0

    while True:
        x = random.random()
        y = random.random()
        dis = (x**2 + y**2)**0.5
        if dis <= 1:
            in_count += 1
        total += 1
        pi_estimate = 4 * in_count / total
        error = abs(pi_estimate - math.pi)

        # 检查当前的误差是否小于或等于给定的阈值 alpha
        if error <= alpha:
            return total  # 返回这时的试验次数 t



if __name__ == "__main__":
    # # 设置最大试验次数和记录间隔
    # # max_trials = 10000000
    # # max_trials = 1000000
    # max_trials = 100000000
    # record_interval = 10000  # 每10000次记录一次
    #
    # # 获取试验次数和误差列表
    # trials, errors = monte_carlo_pi(max_trials, record_interval)
    #
    # # 绘制误差随试验次数的变化图
    # plt.figure(figsize=(10, 5))
    # plt.plot(trials, errors, label='Error', color='blue')
    # plt.xlabel('Number of Trials')
    # plt.ylabel('Absolute Error')
    # plt.title('Error of Pi Estimation Over Trials')
    # plt.grid(True)
    # plt.show()

    # 设定一个误差阈值 alpha
    alpha = 0.01  # 例如，我们想找到误差小于或等于0.01时的试验次数

    # 调用函数
    t = find_min_trials_for_alpha(alpha)

    print(f"Minimum number of trials required to achieve an error <= {alpha} is: {t}")





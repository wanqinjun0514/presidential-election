# for i in range(0, 500001):
#     if i % 10000 == 0:
#         print(i)
from numpy import NaN

# start_time = time.time()
#
# while True:
#     print("正在循环！！！")
#
#     current_time = time.time()
#     if current_time - start_time >= 60:  # 180 秒 = 3 分钟
#         break  # 如果达到三分钟，停止循环（退出程序）
#
# # 可选的结束消息
# print("程序执行了三分钟，现在停止。")

import re

# 推文URL字符串
tweet_url = "https://twitter.com/LindseyGrahamSC/status/1187465914343710720"


# 使用正则表达式提取用户名
username = re.search(r'https://twitter.com/(\w+)/status', tweet_url).group(1)

print(username)  # 输出：mmfa

# print(NaN is None)

import matplotlib.pyplot as plt
import numpy as np

# 创建一个新的图和坐标轴
fig, ax = plt.subplots()

# 设置坐标轴的范围
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# 绘制正方形，其四个点是(0,0), (1,0), (1,1), (0,1)
square = plt.Rectangle((0, 0), 1, 1, fill=False, edgecolor='blue', linewidth=2)
ax.add_patch(square)

# 绘制内切圆，圆心(0.5, 0.5)，半径0.5
circle = plt.Circle((0.5, 0.5), 0.5, fill=False, edgecolor='red', linewidth=2)
ax.add_patch(circle)

# 设置图的标题
# plt.title('Unit Square with an Inscribed Circle')

# 显示图形
plt.show()

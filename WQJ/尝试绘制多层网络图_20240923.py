import matplotlib.pyplot as plt
import networkx as nx

# 创建一个空图
G = nx.DiGraph()

# 添加节点：个体层，组层，社区层
individual_nodes = ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7']
group_nodes = ['G1', 'G2', 'G3']
community_nodes = ['C1']

# 添加各层节点
G.add_nodes_from(individual_nodes, layer='individual')
G.add_nodes_from(group_nodes, layer='group')
G.add_nodes_from(community_nodes, layer='community')

# 添加边：表示不同节点间的关系
# 个体节点到组节点的隶属关系（虚线）
G.add_edges_from([('I1', 'G1'), ('I2', 'G1'), ('I3', 'G2'),
                  ('I4', 'G2'), ('I5', 'G3'), ('I6', 'G3'), ('I7', 'G3')],
                 relation='subordinate')

# 组节点到社区节点的隶属关系（虚线）
G.add_edges_from([('G1', 'C1'), ('G2', 'C1'), ('G3', 'C1')],
                 relation='subordinate')

# 组节点之间的合作关系（实线）
G.add_edges_from([('G1', 'G2'), ('G2', 'G3')], relation='cooperation')

# 分配节点位置：个体、组、社区分层
pos = {}
for i, node in enumerate(individual_nodes):
    pos[node] = (i, 0)  # 个体节点位置 (x, y) 坐标，位于y=0
for i, node in enumerate(group_nodes):
    pos[node] = (i + 1, 1)  # 组节点位于y=1
for i, node in enumerate(community_nodes):
    pos[node] = (1.5, 2)  # 社区节点位于y=2

# 绘制图形
plt.figure(figsize=(10, 8))

# 绘制节点
nx.draw_networkx_nodes(G, pos, nodelist=individual_nodes, node_color='green', label='individual node')
nx.draw_networkx_nodes(G, pos, nodelist=group_nodes, node_color='red', label='group node')
nx.draw_networkx_nodes(G, pos, nodelist=community_nodes, node_color='blue', label='community node')

# 绘制边：区分合作（实线）和隶属关系（虚线）
cooperation_edges = [(u, v) for u, v, d in G.edges(data=True) if d['relation'] == 'cooperation']
subordinate_edges = [(u, v) for u, v, d in G.edges(data=True) if d['relation'] == 'subordinate']

nx.draw_networkx_edges(G, pos, edgelist=cooperation_edges, edge_color='black', label='cooperation', style='solid')
nx.draw_networkx_edges(G, pos, edgelist=subordinate_edges, edge_color='black', label='subordinate', style='dashed')

# 添加标签
nx.draw_networkx_labels(G, pos)

# 添加图例
plt.legend(loc='upper left')
plt.title('Multi-level Network Representation')
plt.axis('off')
plt.show()

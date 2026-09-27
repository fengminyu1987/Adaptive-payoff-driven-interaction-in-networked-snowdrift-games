import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import networkx as nx

file_path = "ER,k=40,r=0.8.xlsx"

r = 0.8
N = 2000  # 节点数
T = 100   # 时间步
W_t = np.zeros((N, N))  # 非对称意愿
R = np.array([[1, 1-r], [1+r, 0]])  # 收益矩阵，0代表合作1代表背叛

avg_degree = 40  # 平均度
p = avg_degree / (N - 1)

all_experiment_data = []


def count_edges(A, strategies):
    cooperator_cooperator_count = 0
    defector_defector_count = 0   
    cooperator_defector_count = 0
    for i in range(N):
        for j in range(i+1, N):
            if A[i, j] == 1:
                if strategies[i] == 0 and strategies[j] == 0:
                    cooperator_cooperator_count += 1
                elif strategies[i] == 1 and strategies[j] == 1:
                    defector_defector_count += 1
                else:
                    cooperator_defector_count += 1
    return cooperator_cooperator_count, defector_defector_count, cooperator_defector_count


def evolve_network(A, strategies, edge_count):
    for i in range(N):
        i_neighbor_indices = np.where(A[i] == 1)[0]
        if len(i_neighbor_indices) == 0:
            continue
        neighbor_index = np.random.choice(i_neighbor_indices)
        neighbor_neighbor_indices = np.where(A[neighbor_index] == 1)[0]
        i_payoffs = np.sum([R[strategies[i]][strategies[k]] for k in i_neighbor_indices])
        neighbor_payoffs = np.sum([R[strategies[neighbor_index]][strategies[k]] for k in neighbor_neighbor_indices])
        mk = max(len(i_neighbor_indices), len(neighbor_neighbor_indices))
        prob = (neighbor_payoffs - i_payoffs) / ((1+r) * mk)
        prob = max(0, prob)
        strategies[i] = np.random.choice([strategies[i], strategies[neighbor_index]], p=[1 - prob, prob])

        for j in range(i+1, N):
            if j == neighbor_index:
                i_payoff = R[strategies[i], strategies[j]]
                j_payoff = R[strategies[j], strategies[i]]
                i_neighbor_payoffs_sum = i_payoffs - i_payoff
                j_neighbor_payoffs_sum = neighbor_payoffs - j_payoff
                W_t[i, j] = 1 / len(i_neighbor_indices) * i_neighbor_payoffs_sum - i_payoff
                W_t[j, i] = 1 / len(neighbor_neighbor_indices) * j_neighbor_payoffs_sum - j_payoff
                alpha_prob = 1 / (1 + np.exp(-0.5 * (W_t[i, j] + W_t[j, i])))
                if np.random.rand() < alpha_prob:
                    action = np.random.choice([1, 2, 3, 4])
                    if action == 1: # 只断
                        A[i, j] = A[j, i] = 0
                        edge_count -= 1
                    elif action == 2:  #
                        i_new_neighbors = [n for n in range(N) if n != i and A[i, n] == 0]
                        if i_new_neighbors:
                            i_new_neighbor = np.random.choice(i_new_neighbors)
                            j_new_neighbors = [n for n in range(N) if n != j and A[j, n] == 0]
                            if j_new_neighbors:
                                j_new_neighbor = np.random.choice(j_new_neighbors)
                                A[i, i_new_neighbor] = A[i_new_neighbor, i] = 1
                                A[j, j_new_neighbor] = A[j_new_neighbor, j] = 1
                                A[i, j] = A[j, i] = 0
                                edge_count += 1
                    elif action == 3:  # i+
                        i_new_neighbors = [n for n in range(N) if n != i and A[i, n] == 0]
                        if i_new_neighbors:
                            i_new_neighbor = np.random.choice(i_new_neighbors)
                            A[i, i_new_neighbor] = A[i_new_neighbor, i] = 1
                            A[i, j] = A[j, i] = 0                         
                    elif action == 4:  # j+
                        j_new_neighbors = [n for n in range(N) if n != j and A[j, n] == 0]
                        if j_new_neighbors:
                            j_new_neighbor = np.random.choice(j_new_neighbors)
                            A[j, j_new_neighbor] = A[j_new_neighbor, j] = 1
                            A[i, j] = A[j, i] = 0
            else:
                if A[i, j] == 1:
                    j_neighbor_indices = np.where(A[j] == 1)[0]
                    i_payoff = R[strategies[i], strategies[j]]
                    j_payoff = R[strategies[j], strategies[i]]
                    i_neighbor_payoffs_sum = i_payoffs - i_payoff
                    j_neighbor_payoffs_sum = np.sum([R[strategies[j], strategies[k]] for k in j_neighbor_indices if k != i])
                    W_t[i, j] = 1 / len(i_neighbor_indices) * i_neighbor_payoffs_sum - i_payoff
                    W_t[j, i] = 1 / len(j_neighbor_indices) * j_neighbor_payoffs_sum - j_payoff
                    alpha_prob = 1 / (1 + np.exp(-0.5 * (W_t[i, j] + W_t[j, i])))
                    if np.random.rand() < alpha_prob:
                        action = np.random.choice([1, 2, 3, 4])
                        if action == 1: # 只断
                            A[i, j] = A[j, i] = 0
                            edge_count -= 1
                        elif action == 2:  #
                            i_new_neighbors = [n for n in range(N) if n != i and A[i, n] == 0]
                            if i_new_neighbors:
                                i_new_neighbor = np.random.choice(i_new_neighbors)
                                j_new_neighbors = [n for n in range(N) if n != j and A[j, n] == 0]
                                if j_new_neighbors:
                                    j_new_neighbor = np.random.choice(j_new_neighbors)
                                    A[i, i_new_neighbor] = A[i_new_neighbor, i] = 1
                                    A[j, j_new_neighbor] = A[j_new_neighbor, j] = 1
                                    A[i, j] = A[j, i] = 0
                                    edge_count += 1
                        elif action == 3:  # i+
                            i_new_neighbors = [n for n in range(N) if n != i and A[i, n] == 0]
                            if i_new_neighbors:
                                i_new_neighbor = np.random.choice(i_new_neighbors)
                                A[i, i_new_neighbor] = A[i_new_neighbor, i] = 1
                                A[i, j] = A[j, i] = 0                         
                        elif action == 4:  # j+
                            j_new_neighbors = [n for n in range(N) if n != j and A[j, n] == 0]
                            if j_new_neighbors:
                                j_new_neighbor = np.random.choice(j_new_neighbors)
                                A[j, j_new_neighbor] = A[j_new_neighbor, j] = 1
                                A[i, j] = A[j, i] = 0
    return edge_count


for _ in range(20):
    strategies = np.random.randint(2, size=N) # 存储玩家策略的数组
    edge_count = 0
    G = nx.erdos_renyi_graph(N, p)
    A = nx.to_numpy_array(G)
    
    # 初始边数
    edge_count = np.sum(A) // 2  # 无向图除以2
      
    # 初始合作者
    initial_cooperator_count = np.sum(strategies == 0)
    initial_cooperator_ratio = initial_cooperator_count / N
    print(initial_cooperator_count)


    
    # 初始不同类型边
    cooperator_cooperator_count, defector_defector_count, cooperator_defector_count = count_edges(A, strategies)
    cooperator_cooperator_ratios = cooperator_cooperator_count / edge_count
    cooperator_defector_ratios = cooperator_defector_count / edge_count
    defector_defector_ratios = defector_defector_count / edge_count

    # 存储初始数据
    data = [[edge_count, cooperator_cooperator_ratios, cooperator_defector_ratios, defector_defector_ratios, initial_cooperator_ratio]]

    for t in range(T-1):
        # 总边数
        edge_count = evolve_network(A, strategies, edge_count)
        # 各类型边
        cooperator_cooperator_count, defector_defector_count, cooperator_defector_count = count_edges(A, strategies)
        cooperator_cooperator_ratios = cooperator_cooperator_count / edge_count
        cooperator_defector_ratios = cooperator_defector_count / edge_count
        defector_defector_ratios = defector_defector_count / edge_count
        
        # 合作者比例
        cooperator_count = np.sum(strategies == 0)
        cooperator_ratio = cooperator_count / N
        print(cooperator_count)
        
        # 存储每个时间步的数据
        data.append([edge_count, cooperator_cooperator_count, cooperator_defector_ratios, defector_defector_count, cooperator_ratio])

    all_experiment_data.append(data)

average_data = np.mean(all_experiment_data, axis=0)
df = pd.DataFrame(average_data, columns=['Edge Count', 'C-C', 'C-D', 'D-D', 'fc'])
df.to_excel(file_path)



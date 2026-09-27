import numpy as np
import pandas as pd
import networkx as nx

file_path = "du_WS_k4_r0.9.xlsx"

r = 0.9
N = 2000  # 节点数
T = 260   # 时间步
W_t = np.zeros((N, N))  # 非对称意愿
R = np.array([[1, 1-r], [1+r, 0]])  # 收益矩阵，0代表合作1代表背叛

final_cooperator_degree_distributions = []
final_defector_degree_distributions = []

def evolve_network(A, strategies):
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

def degree_distribution(A, strategies):
    degrees = np.sum(A, axis=0)
    cooperator_degrees = degrees[np.where(strategies == 0)[0]]
    defector_degrees = degrees[np.where(strategies == 1)[0]]
    return cooperator_degrees, defector_degrees

def degree_distribution1(A):
    degrees = np.sum(A, axis=0)
    return degrees

strategies = np.random.randint(2, size=N) # 存储玩家策略的数组
G = nx.random_graphs.random_regular_graph(4, N)
A = nx.to_numpy_array(G)

# 进化网络
for t in range(T-1):       
    evolve_network(A, strategies)
    
final_cooperator_degrees, final_defector_degrees = degree_distribution(A, strategies)
final_degree_distribution = degree_distribution1(A)

# 计算合作者和背叛者的度分布
final_cooperator_distribution = np.bincount(final_cooperator_degrees.astype(int)) / len(final_cooperator_degrees)
final_defector_distribution = np.bincount(final_defector_degrees.astype(int)) / len(final_defector_degrees)
final_distribution = np.bincount(final_degree_distribution.astype(int)) / len(final_degree_distribution)

# 将结果保存到Excel文件
max_length = max(len(final_cooperator_distribution), len(final_defector_distribution))
final_cooperator_distribution = np.pad(final_cooperator_distribution, (0, max_length - len(final_cooperator_distribution)), mode='constant')
final_defector_distribution = np.pad(final_defector_distribution, (0, max_length - len(final_defector_distribution)), mode='constant')
final_distribution = np.pad(final_distribution, (0, max_length - len(final_distribution)), mode='constant')

df = pd.DataFrame({
    'Degree': np.arange(max_length),
    'Final Distribution': final_distribution,
    'Final Cooperator Distribution': final_cooperator_distribution,
    'Final Defector Distribution': final_defector_distribution
})

df.to_excel(file_path, index=False)

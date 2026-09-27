import numpy as np
import pandas as pd
import networkx as nx

def evolve_network(strategies):
    for i in range(N):
        i_neighbor_indices = list(G.neighbors(i))
        if len(i_neighbor_indices) == 0:
            continue
        neighbor_index = np.random.choice(i_neighbor_indices)
        neighbor_neighbor_indices = list(G.neighbors(neighbor_index))
        i_payoffs = np.sum([R[strategies[i]][strategies[k]] for k in i_neighbor_indices])
        neighbor_payoffs = np.sum([R[strategies[neighbor_index]][strategies[k]] for k in neighbor_neighbor_indices])
        mk = max(len(i_neighbor_indices), len(neighbor_neighbor_indices))
        prob = (neighbor_payoffs - i_payoffs) / ((1+r) * mk)
        prob = max(0, prob)
        strategies[i] = np.random.choice([strategies[i], strategies[neighbor_index]], p=[1 - prob, prob])

for r in np.arange(0.0, 1.1, 0.1): 
    file_path = f"TWS,k=10,r={r}.xlsx"
    N = 2000  # 节点数
    T = 200   # 时间步
    W_t = np.zeros((N, N))  # 非对称意愿
    R = np.array([[1, 1-r], [1+r, 0]])  # 收益矩阵，0代表合作1代表背叛        
    all_experiment_data = []
    
    for k in range(4):
        strategies = np.random.randint(2, size=N) # 存储玩家策略的数组
        G = nx.watts_strogatz_graph(N, k=10, p=0.1)
         # 初始合作者
        initial_cooperator_count = np.sum(strategies == 0)
        print(k, "-", initial_cooperator_count)
        data = [[initial_cooperator_count]]
        for t in range(T-1):       
            # 合作者比例
            cooperator_count = np.sum(strategies == 0)
            print(cooperator_count)
           
            evolve_network(strategies)
            data.append([cooperator_count])
        all_experiment_data.append(data)
            
    average_data = np.mean(all_experiment_data, axis=0)
    df = pd.DataFrame(average_data/2000, columns=['fc'])
    df.to_excel(file_path)
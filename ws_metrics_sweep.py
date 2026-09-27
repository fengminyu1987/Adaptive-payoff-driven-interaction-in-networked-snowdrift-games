
import numpy as np
import pandas as pd
import networkx as nx

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

def calculate_metrics(G):
    if nx.is_connected(G):
        avg_clustering = nx.average_clustering(G)
        avg_shortest_path = nx.average_shortest_path_length(G)
    else:
        components = sorted(nx.connected_components(G), key=len, reverse=True)
        largest_component = G.subgraph(components[0])
        avg_clustering = nx.average_clustering(largest_component)
        avg_shortest_path = nx.average_shortest_path_length(largest_component)
    lcc_size = len(max(nx.connected_components(G), key=len))
    return avg_clustering, avg_shortest_path, lcc_size

avg_clustering_values = []
avg_shortest_path_values = []
lcc_size_values = []

for r in np.arange(0.6, 0.8, 0.1): 
    file_path = f"WS_k=10_r={r}.xlsx"
    N = 2000  # 节点数
    T = 270   # 时间步
    num_runs = 6  # 运行次数
    W_t = np.zeros((N, N))  # 非对称意愿
    R = np.array([[1, 1-r], [1+r, 0]])  # 收益矩阵，0代表合作1代表背叛
    
    results = []
    
    for n in range(num_runs):
        G = nx.watts_strogatz_graph(N, k=10, p=0.1)
        A = nx.to_numpy_array(G)
        strategies = np.random.randint(2, size=N)
        print(n)
    
        last_20_avg_clustering = []
        last_20_avg_shortest_path = []
        last_20_lcc_size = []
    
        for t in range(T):
            evolve_network(A, strategies)
            if t >= T - 20:
                G = nx.from_numpy_array(A)  # 将邻接矩阵转换为图
                avg_clustering, avg_shortest_path, lcc_size = calculate_metrics(G)
                last_20_avg_clustering.append(avg_clustering)
                last_20_avg_shortest_path.append(avg_shortest_path)
                last_20_lcc_size.append(lcc_size)
    
        avg_clustering = np.mean(last_20_avg_clustering)
        avg_shortest_path = np.mean(last_20_avg_shortest_path)
        avg_lcc_size = np.mean(last_20_lcc_size)
        results.append((avg_clustering, avg_shortest_path, avg_lcc_size))
    
    avg_avg_clustering = np.mean([res[0] for res in results])
    avg_avg_shortest_path = np.mean([res[1] for res in results])
    avg_avg_lcc_size = np.mean([res[2] for res in results])
    
    df = pd.DataFrame({
        'Run': np.arange(1, num_runs + 1),
        'Average Clustering Coefficient': [avg[0] for avg in results],
        'Average Shortest Path Length': [avg[1] for avg in results],
        'Largest Connected Component Size': [avg[2] for avg in results]
    })
    
    df.loc[num_runs] = ['Average', avg_avg_clustering, avg_avg_shortest_path, avg_avg_lcc_size]
    
    df.to_excel(file_path, index=False)

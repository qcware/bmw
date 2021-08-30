import bmw
import numpy as np

problem = bmw.TestCarProblem.parse_problem(filepath='../../data/3-refined')

types, test_set = bmw.TestCarProblemTranslater.translate_problem(problem=problem)

S = np.zeros((types[0].nfeature,)*2, dtype=np.bool)

for test in test_set.expressions:
    indices = []
    for expression in test.expressions:
        indices += expression.indices
    for i in indices:
        for j in indices:
            S[i, j] = True

for typ in types:
    for group in typ.groups:
        for i in group:
            for j in group:
                S[i, j] = True

# for typ in types:
#     for rule in typ.rules:
#         indices = rule.predicate.indices
#         for i in indices:
#             for j in indices:
#                 S[i, j] = True
#         indices = rule.implication.indices
#         for i in indices:
#             for j in indices:
#                 S[i, j] = True

clusters = []
seen = []
    
for i in range(S.shape[0]):
    if i in seen: continue
    neighbor_list = [i]
    cluster = []
    while len(neighbor_list):
        pivot = neighbor_list[0]
        neighbor_list = neighbor_list[1:]
        cluster.append(pivot) 
        new_neighbors = [index for index, value in enumerate(S[pivot,:]) if value]
        neighbor_list += [_ for _ in new_neighbors if _ not in neighbor_list and _ not in cluster]
    clusters.append(cluster)
    seen += cluster

clusters = list(sorted(clusters, key = lambda x : -len(x)))
        
print(clusters) 

for cluster in clusters:
    print(len(cluster))
print(sum([len(_) for _ in clusters]))
        




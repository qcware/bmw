import bmw
import numpy as np

import sys
key = sys.argv[1]

problem = bmw.Problem.parse(filepath='../../data/3-refined')

dat = np.load('../2-prod/test-0.npz')
constellation = dat['constellation']
constellation_type_indices = dat['constellation_type_indices']

# Only use our best 60 constellation
constellation = constellation[:60, :]
constellation_type_indices = constellation_type_indices[:60]

dat2 = np.load('../3-sched/final.npz')
test_indices = dat2['test_indices']
car_indices = dat2['car_indices']

tests_performed = [[] for _ in range(len(constellation))]
for test_index, car_index in zip(np.ravel(test_indices), np.ravel(car_indices)):
    if test_index == -1: continue
    tests_performed[car_index].append(test_index)

for iteration in range(20000):

    print(np.sum(constellation))

    car_index = np.random.randint(60)
    car = constellation[car_index].copy()

    feature_indices = np.where(car)[0]
    
    feature_index = np.random.randint(len(feature_indices))

    car[feature_indices[feature_index]] = False

    if not problem.type_specifications[constellation_type_indices[car_index]].check_valid(car):
        continue

    passes = True
    for test_index in tests_performed[car_index]:
        if not problem.test_set.expressions[test_index].evaluate(car):
            passes = False
            break

    if not passes: continue

    constellation[car_index] = car
            
np.savez(
    'test-%s.npz' % key,
    constellation=constellation,
    constellation_type_indices=constellation_type_indices,
    )
    

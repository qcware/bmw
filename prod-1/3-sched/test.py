import bmw
import numpy as np

problem = bmw.Problem.parse(filepath='../../data/3-refined')

dat = np.load('../2-prod/test-0.npz')
constellation = dat['constellation']
constellation_type_indices = dat['constellation_type_indices']

test_indices = np.argsort(problem.test_groups)

for tindex2, tindex1 in enumerate(test_indices):

    expression = problem.test_set.expressions[tindex1]
    count = problem.test_set.counts[tindex1]

    passes = [index for index, state in enumerate(constellation) if expression.evaluate(state)]

    print('%3d : %3d %1d : %3d %3d' % (
        tindex2, 
        tindex1, 
        problem.test_groups[tindex1],
        len(passes), 
        count,
        ))

    
test_array = np.zeros((10, 100))
test_array[...] = -1

car_array = np.zeros((10, 100))
car_array[...] = -1

time_index = 0
slot_index = 0

for test_index in test_indices:

    expression = problem.test_set.expressions[test_index]
    count = problem.test_set.counts[test_index]

    car_candidates = [index for index, state in enumerate(constellation) if expression.evaluate(state)]

    ncar = 0
    
    for car_index in car_candidates:
        
        if car_index in car_array[time_index, :slot_index]: continue

        test_array[slot_index, time_index] = test_index
        car_array[slot_index, time_index] = car_index

        ncar += 1

        if ncar == count: break

        slot_index += 1
        if slot_index == test_indices.shape[0]:
            slot_index = 0
            time_index += 1

    print(car_array[:, :7])
    print(car_candidates)

    if ncar < count: 
        raise RuntimeError('Cannot satisfy test')

        

    
    
    

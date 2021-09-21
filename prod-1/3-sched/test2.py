import bmw
import numpy as np

problem = bmw.Problem.parse(filepath='../../data/3-refined')

dat = np.load('../2-prod/test-0.npz')
constellation = dat['constellation']
constellation_type_indices = dat['constellation_type_indices']

metric = np.array([10 * problem.test_groups[index] - problem.test_set.counts[index] for index in range(len(problem.test_groups))])

# test_indices = np.argsort(problem.test_groups)
test_indices = np.argsort(metric)

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

    
test_array = np.zeros((10, 400))
test_array[...] = -1

car_array = np.zeros((10, 400))
car_array[...] = -1

time_index = 0
slot_index = 0

counter = 0

while len(test_indices):
    
    if counter > 3000:
        break
    counter += 1

    for test_index in test_indices:

        expression = problem.test_set.expressions[test_index]
        count = problem.test_set.counts[test_index]

        car_candidates = [index for index, state in enumerate(constellation) if expression.evaluate(state)]

        np.random.shuffle(car_candidates)

        # TODO: Try a different test if we can't fill
    
        found = False
        for car_index in car_candidates:
            if car_index in car_array[:slot_index, time_index]: continue
            car_array[slot_index, time_index] = car_index
            test_array[slot_index, time_index] = test_index
            slot_index += 1
            if slot_index == test_array.shape[0]:
                slot_index = 0
                time_index += 1
            found = True
            break


        if not found: 
            slot_index = 0
            time_index += 1
        else:
            # test_indices = test_indices[1:]
            print(count, np.sum(test_array == test_index))
            if np.sum(test_array == test_index) >= count:
                test_indices = test_indices[1:]
            break

        
print(car_array[:, :20])

s = ''
for col_index, col in enumerate(car_array.T):
    # print(row)

    if np.max(col) < 0.0: break

    v = ''.join([' ' if _ == -1 else 'O' for _ in col])
    print('%3d: %s' % (col_index, v))
    # s += ''.join([' ' if _ == -1 else 'O' for _ in row])
    # s += '\n'

# print(s)




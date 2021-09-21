import bmw
import numpy as np

problem = bmw.Problem.parse(filepath='../../data/3-refined')

dat = np.load('../2-prod/test-0.npz')
constellation = dat['constellation']
constellation_type_indices = dat['constellation_type_indices']

# Only use our best 60 constellation
constellation = constellation[:60, :]
constellation_type_indices = constellation_type_indices[:60]

# Sort to prioritize early test groups (first priority) with large counts (second priority)
metric = np.array([10 * problem.test_groups[index] - problem.test_set.counts[index] for index in range(len(problem.test_groups))])
test_indices = list(np.argsort(metric))

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

nslot = 10

test_counts = np.zeros_like(test_indices)

test_array = []
car_array = []

test_slot = []
car_slot = []

while len(test_indices):

    nuke_slot = True
    
    for t2, test_index in enumerate(test_indices):

        group_index = problem.test_groups[test_index]

        expression = problem.test_set.expressions[test_index]
        count = problem.test_set.counts[test_index]

        car_candidates = [index for index, state in enumerate(constellation) if expression.evaluate(state)]

        np.random.shuffle(car_candidates)

        found = False
        for car_index in car_candidates:
            if car_index in car_slot: continue
            
            # Check DAG Rules
            breaks_dag = False
            for time_index in range(len(test_array)):
                if not car_index in car_array[time_index]: continue
                slot_index = car_array[time_index].index(car_index)
                test_index2 = test_array[time_index][slot_index] 
                group_index2 = problem.test_groups[test_index2]
                if group_index < group_index2:
                    breaks_dag = True
                    break
            if breaks_dag: continue

            test_slot.append(test_index)
            car_slot.append(car_index)
            test_counts[test_index] += 1
            if len(test_slot) == nslot:
                test_array.append(test_slot)
                car_array.append(car_slot)      
                test_slot = []
                car_slot = []
            found = True
            nuke_slot = False
            break

        if found:
            if test_counts[test_index] == count: 
                test_indices.pop(t2) 
                break

    if nuke_slot:
        test_array.append(test_slot)
        car_array.append(car_slot)      
        test_slot = []
        car_slot = []

test_array.append(test_slot)
car_array.append(car_slot)
        
print('Test Groups:\n')
for time, test_slot in enumerate(test_array):        
    print('%-3d : %s' % (time, ''.join([str(problem.test_groups[test_index]) for test_index in test_slot])))
print('')

print('Car Indices:\n')
for time, car_slot in enumerate(car_array):
    print('%-3d : %s' % (time, ' '.join(['%3d' % car_index for car_index in car_slot])))
print('')

print('Test Indices:\n')
for time, test_slot in enumerate(test_array):
    print('%-3d : %s' % (time, ' '.join(['%3d' % test_index for test_index in test_slot])))
print('')

print('Test Count Checks:\n')
for t2 in range(len(test_counts)):
    print('%-3d : %1d %1d %r' % (t2, problem.test_set.counts[t2], test_counts[t2], 
        problem.test_set.counts[t2] == test_counts[t2]))
print('')

print(np.sum(problem.test_set.counts))
    







import bmw
import numpy as np

np.set_printoptions(threshold=np.inf)

problem = bmw.Problem.parse(filepath='../../../data/3-refined')

# Each car can be used once per day. Check for repeated cars in slot
with open('carindices.txt') as f:
    car_indices = []
    lines = f.readlines()
    for line in lines:
        i_slot, cars = line.split(' :  ',1)
        cars = cars.split()
        if len(cars) != len(set(cars)):
            print('Slot %d has duplicate cars' % i_slot)
        for i in cars:
            car_indices.append(i)

# Check for dependent test group invalidations
with open('testindices.txt') as f:
    test_indices = []
    lines = f.readlines()
    for line in lines:
        i_slot, tests = line.split('  : ',1)
        tests = tests.split()
        for i in tests:
            test_indices.append(i)

with open('testgroups.txt') as f:
    test_groups = []
    lines = f.readlines()
    for line in lines:
        i_slot, groups = line.split('  : ',1)
        groups = groups.strip('\n')
        for i_test in groups:
            test_groups.append(i_test)

prev = 0
for index in range(len(test_groups)):
    current = int(test_groups[index])
    if current < prev:
        print('test group %d performed after %d' % (current,prev))
        current_car_index = int(car_indices[index])
        print('Current car is %d at slot %d' % (current_car_index,index))
        for cindex in range(index+1):
            icar = int(car_indices[cindex])
            if icar == current_car_index:
                itest = int(test_indices[cindex])
                problem_test_group = problem.test_groups[itest]
                print('Car %d was underwent test %d of group %d at previous slot %d' % (
                      current_car_index,itest,problem_test_group,cindex))
    prev = current

# Check if test not satisfying number of cars


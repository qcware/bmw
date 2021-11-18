import bmw 
import numpy as np
import matplotlib.pyplot as plt 

problem = bmw.Problem.parse(filepath='../../../data/3-refined')

dat1 = np.load('../../2-prod/test-0.npz')
constellation1 = dat1['constellation']
constellation_type_indices1 = dat1['constellation_type_indices']

dat2 = np.load('../test-0.npz')
constellation2 = dat2['constellation']

constellation1 = constellation1[:60, :]
constellation_type_indices1 = constellation_type_indices1[:60]

metric = np.array([10 * problem.test_groups[index] - problem.test_set.counts[index] for index in range(len(problem.test_groups))])
test_indices = list(np.argsort(metric))

x = np.zeros(60,dtype=int)
for index in range(60):
    x[index] = index

y1 = np.zeros(60,dtype=int)
y2 = np.zeros(60,dtype=int)
for t2, test_index in enumerate(test_indices):

    expression = problem.test_set.expressions[test_index]

    car_candidates1 = [index for index, state in enumerate(constellation1) if expression.evaluate(state)]
    for ii1, value1 in enumerate(car_candidates1):
        y1[value1] += 1

    car_candidates2 = [index for index, state in enumerate(constellation2) if expression.evaluate(state)]
    for ii2, value2 in enumerate(car_candidates2):
        y2[value2] += 1


plt.rcParams.update({'font.size': 8})
plt.clf()
plt.bar(x,y1,color='b',label='Phase 1')
plt.bar(x,y2,color='r',label='Phase 2')
plt.axis([-1, 60, 50, 250])
plt.yticks(np.arange(0, 250+1, 50))
plt.legend(loc=1)
plt.xlabel('Test Car')
plt.ylabel('Number of Test Rules Satisfied')
plt.savefig('rules.pdf',bbox_inches='tight')



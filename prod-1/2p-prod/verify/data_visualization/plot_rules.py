import bmw 
import numpy as np
import matplotlib.pyplot as plt 

problem = bmw.Problem.parse(filepath='../../../../data/3-refined')

dat = np.load('../../test-6.npz')
constellation = dat['constellation']
constellation_type_indices = dat['constellation_type_indices']


constellation = constellation[:62, :]
constellation_type_indices = constellation_type_indices[:62]

metric = np.array([10 * problem.test_groups[index] - problem.test_set.counts[index] for index in range(len(problem.test_groups))])
test_indices = list(np.argsort(metric))


x = np.zeros(62,dtype=int)
for index in range(62):
    x[index] = index


y = np.zeros(62,dtype=int)
for t2, test_index in enumerate(test_indices):

    expression = problem.test_set.expressions[test_index]

    car_candidates = [index for index, state in enumerate(constellation) if expression.evaluate(state)]
    for ii, value in enumerate(car_candidates):
        y[value] += 1


plt.rcParams.update({'font.size': 8})
plt.clf()
plt.bar(x,y,color='r',label='Phase 2')
plt.axis([-1, 62, 50, 250])
plt.yticks(np.arange(0, 250+1, 50))
plt.legend(loc=1)
plt.xlabel('Test Vehicle')
plt.ylabel('Number of Test Rules Satisfied Per Test Vehicle')
plt.savefig('rules-6.pdf',bbox_inches='tight')



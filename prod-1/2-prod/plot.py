import numpy as np
import matplotlib.pyplot as plt

max_score = 644

scores1 = np.loadtxt('../../sandbox/leapfrog/test7-npass.dat')
scores2 = np.loadtxt('test-0-npass.txt')

print(scores2[58])
print(scores2[59])
print(scores2[60])

plt.clf()
# plt.plot(np.arange(len(scores1)) + 1, scores1, 'o--b', label='QC Ware Heuristic #1')
plt.plot(np.arange(len(scores2)) + 1, scores2, 'o--b', label='QC Ware Solution')
plt.plot([0, 70], [644, 644], '-k', label='Max Possible Score')
plt.plot([60, 60], [0, 644], '--k', label='SAT Bound')
plt.legend(loc=3)
plt.axis([0, 70, 0, 650])
plt.xlabel('Number of Test Cars in Constellation')
plt.ylabel('Score: Number of Tests Covered by Constellation')
plt.grid(True)
plt.savefig('test.pdf')

import numpy as np
import matplotlib.pyplot as plt

max_score = 644

scores1 = np.loadtxt('../2-prod/test-0-npass.txt')
scores2 = np.loadtxt('test-6-npass.txt')

plt.clf()
plt.plot(np.arange(len(scores1)) + 1, scores1, 'o--b', label='QC Ware Solution Phase 1')
#plt.plot(np.arange(len(scores2)) + 1, scores2, 'o--r', label='QC Ware Solution Phase 2')
plt.plot([0, 70], [644, 644], '-k', label='Max Possible Score')
plt.plot([60, 60], [0, 644], '--k', label='SAT Bound')
plt.legend(loc=8)
plt.axis([0, 70, 0, 650])
plt.xlabel('Number of Test Vehicles in Constellation')
plt.ylabel('Score: Number of Tests Covered by Constellation')
plt.grid(True)
plt.savefig('constrained_maxsat_1.pdf')

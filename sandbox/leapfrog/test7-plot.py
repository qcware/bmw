import numpy as np
import matplotlib.pyplot as plt

max_score = 644

scores = np.loadtxt('test7-npass.dat')

print(scores)

plt.clf()
plt.plot(np.arange(len(scores)) + 1, scores, 's--', label='QC Ware Heuristic')
plt.plot([0, 70], [644, 644], '-k', label='Max Possible Score')
plt.legend(loc=4)
plt.axis([0, 70, 0, 650])
plt.xlabel('Number of Test Cars in Constellation')
plt.ylabel('Score: Number of Tests Covered by Constellation')
plt.savefig('test7-npass.pdf')

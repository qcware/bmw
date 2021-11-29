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


x = np.zeros(60,dtype=int)
y1 = np.zeros(60,dtype=int)
y2 = np.zeros(60,dtype=int)
for index in range(60):
    x[index] = index
    y1[index] = np.sum(constellation1[index,:])
    y2[index] = np.sum(constellation2[index,:])


plt.rcParams.update({'font.size': 8})
plt.clf()
plt.bar(x,y1,color='b',label='Phase 1')
plt.bar(x,y2,color='r',label='Phase 2')
plt.axis([-1, 60, 50, 100])
plt.yticks(np.arange(0, 100+1, 50))
plt.legend(loc=1)
plt.xlabel('Test Vehicle')
plt.ylabel('Number of Features Per Test Vehicle')
plt.savefig('hamming_2.pdf',bbox_inches='tight')



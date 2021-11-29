import numpy as np
import matplotlib.pyplot as plt


sol = np.load('../../test-0.npz')
constellation = sol['constellation']
constellation_type_indices = sol['constellation_type_indices']


x = np.zeros(60,dtype=int)
y = np.zeros(60,dtype=int)
for car_i in range(60):
    x[car_i] = car_i
    y[car_i] = sum(constellation[car_i][:])

plt.rcParams.update({'font.size': 8})

plt.clf()
#plt.plot(x,y,'o', c='mediumblue', markersize=2)
plt.bar(x,y,color='b',label='Phase 1')
plt.axis([-1, 60, 50, 100])
plt.yticks(np.arange(0, 100+1, 10))
#axes=plt.gca()
#axes.set_aspect('equal')
plt.legend(loc=1)
plt.xlabel('Test Vehicle')
plt.ylabel('Number of Features Per Test Vehicle')
#plt.legend(loc=1)
plt.savefig('hamming.pdf',bbox_inches='tight')


import numpy as np
import matplotlib.pyplot as plt


sol = np.load('../../test-6.npz')
constellation = sol['constellation']
constellation_type_indices = sol['constellation_type_indices']


x = np.zeros(62,dtype=int)
y = np.zeros(62,dtype=int)
for car_i in range(62):
    x[car_i] = car_i
    y[car_i] = sum(constellation[car_i][:])

plt.rcParams.update({'font.size': 8})

plt.clf()
#plt.plot(x,y,'o', c='mediumblue', markersize=2)
plt.bar(x,y,color='b')
plt.axis([-1, 62, 50, 100])
plt.yticks(np.arange(0, 100+1, 10))
#axes=plt.gca()
#axes.set_aspect('equal')
plt.xlabel('Test Car')
plt.ylabel('Hamming Weight')
#plt.legend(loc=1)
plt.savefig('hamming-6.pdf',bbox_inches='tight')


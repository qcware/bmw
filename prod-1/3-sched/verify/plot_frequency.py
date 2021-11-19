import bmw 
import numpy as np
import matplotlib.pyplot as plt 


with open('carindices.txt') as f:
    car_indices = []
    lines = f.readlines()
    for line in lines:
        i_slot, cars = line.split(' :  ',1)
        cars = cars.split()
        for i in cars:
            car_indices.append(int(i))
car_indices = np.array(car_indices)

x = np.zeros(60,dtype=int)
y = np.zeros(60,dtype=int)
for car in range(60):
    x[car] = car

    freq = np.count_nonzero(car_indices == car)
    y[car] = freq

plt.rcParams.update({'font.size': 8})
plt.clf()
#plt.bar(x,y,color='b',label='Phase 1')
plt.bar(x,y,color='b')
plt.axis([-1, 60, 0, 60])
plt.yticks(np.arange(0, 60+1, 10))
#plt.legend(loc=1)
plt.xlabel('Test Car')
plt.ylabel('Number of Scheduled Tests')
plt.savefig('frequency.pdf',bbox_inches='tight')


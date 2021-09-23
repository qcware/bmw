import numpy as np
import matplotlib.pyplot as plt


with open('testgroups.txt') as f:
    test_day = []
    test_slot = []
    test_group = []
    lines = f.readlines()
    for line in lines:
        i_slot, groups = line.split('  : ',1)
        groups = groups.strip('\n')
        slot = 1
        for i_test in groups:
            test_day.append(i_slot)
            test_group.append(i_test)
            test_slot.append(slot)
            slot += 1

x1 = []
y1 = []
x2 = []
y2 = []
x3 = []
y3 = []
x4 = []
y4 = []
x5 = []
y5 = []
for i in range(len(test_slot)):
    if int(test_group[i]) == 1:
        x1.append(int(test_day[i]))
        y1.append(int(test_slot[i]))
    if int(test_group[i]) == 2:
        x2.append(int(test_day[i]))
        y2.append(int(test_slot[i]))
    if int(test_group[i]) == 3:
        x3.append(int(test_day[i]))
        y3.append(int(test_slot[i]))
    if int(test_group[i]) == 4:
        x4.append(int(test_day[i]))
        y4.append(int(test_slot[i]))
    if int(test_group[i]) == 5:
        x5.append(int(test_day[i]))
        y5.append(int(test_slot[i]))

plt.rcParams.update({'font.size': 8})

plt.clf()
plt.plot(x1,y1,'s', c='mediumblue', markersize=2, label='Group 1')
plt.plot(x2,y2,'s', c='violet', markersize=2, label='Group 2')
plt.plot(x3,y3,'s', c='forestgreen', markersize=2, label='Group 3')
plt.plot(x4,y4,'s', c='lightskyblue', markersize=2, label='Group 4')
plt.plot(x5,y5,'s', c='red', markersize=2, label='Group 5')
plt.axis([-1, 80, 0, 11])
plt.yticks(np.arange(1, 10+1, 9))
axes=plt.gca()
axes.set_aspect('equal')
plt.xlabel('Test Day')
#plt.ylabel('Test Slot')
plt.ylabel('Number\nof Tests')
#plt.legend(loc=1)
plt.savefig('scheduling2.pdf',bbox_inches='tight')


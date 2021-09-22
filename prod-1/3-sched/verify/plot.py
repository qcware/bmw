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



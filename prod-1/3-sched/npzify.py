import numpy as np
import re

lines = open('final.txt').readlines()

indexA = [index for index, line in enumerate(lines) if re.match(r'^\s*Test Groups:\s*$', line)][0]
indexB = [index for index, line in enumerate(lines) if re.match(r'^\s*Car Indices:\s*$', line)][0]
indexC = [index for index, line in enumerate(lines) if re.match(r'^\s*Test Indices:\s*$', line)][0]

test_groups = []
linesA = lines[indexA+2:indexA+2+78]
for line in linesA:
    mobj = re.match('^\s*(\d+)\s*:\s*(\S+)\s*$', line)
    contents = [int(_) for _ in mobj.group(2)]
    contents += [-1]*(10 - len(contents))
    test_groups.append(contents)
test_groups = np.array(test_groups)

car_indices = []
linesB = lines[indexB+2:indexB+2+78]
for line in linesB:
    mobj = re.match('^\s*(\d+)\s*:\s*(.*)\s*$', line)
    contents = [int(_) for _ in mobj.group(2).split()]
    contents += [-1]*(10 - len(contents))
    car_indices.append(contents)
car_indices = np.array(car_indices)

test_indices = []
linesC = lines[indexC+2:indexC+2+78]
for line in linesC:
    mobj = re.match('^\s*(\d+)\s*:\s*(.*)\s*$', line)
    contents = [int(_) for _ in mobj.group(2).split()]
    contents += [-1]*(10 - len(contents))
    test_indices.append(contents)
test_indices = np.array(test_indices)

np.savez('final.npz',
    test_groups=test_groups,
    car_indices=car_indices,
    test_indices=test_indices,
    )

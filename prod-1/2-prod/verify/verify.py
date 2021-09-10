import bmw 
import numpy as np

# Load solution bmw/prod-1/2-prod/test-0.npz
sol = np.load('../test-0.npz')
#print(sorted(sol.files))
constellation = sol['constellation']
constellation_type_indices = sol['constellation_type_indices']

# Compare against data bmw/data/2-polished/
#dat = bmw.Problem.parse(filepath='../../../data/2-polished')
#  2-polished doesn't contain test_groups
#groups = bmw.TestCarProblemParser.parse_groups(filename='../../../data/2-polished/groups.txt')
#  parser from old-bmw 

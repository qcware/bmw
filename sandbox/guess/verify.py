import bmw
import numpy as np

problem = bmw.Problem.parse(filepath='../../data/3-refined')

dat = np.load('test.npz')

type_indices = dat['type_indices']
states = dat['states']
masks = dat['masks']

for tindex, expression in enumerate(problem.test_set.expressions):

    if not problem.type_specifications[type_indices[tindex]].check_valid(states[tindex]):
        raise RuntimeError('Invalid type')

    if not expression.evaluate(states[tindex]):
        raise RuntimeError('Invalid test')
    
    mask = [False]*len(states[tindex])
    for expression in expression.expressions:
        for index in expression.indices:
            mask[index] = True

    if list(mask) != list(masks[tindex]):
        raise RuntimeError('Invalid mask')

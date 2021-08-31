import bmw
import numpy as np

problem = bmw.Problem.parse(filepath='../../data/3-refined')

# Guess for pool
dat = np.load('../1-guess/test.npz')
pool_type_indices = dat['type_indices']
pool_states = dat['states']
pool_masks = dat['masks']

max_ncar = 70
niteration = 10000

current_test_set = problem.test_set

constellation = []
constellation_type_indices = []

generator = bmw.RandomStateGenerator.build_random_seed()

for k in range(max_ncar):

    print('ncar %d:' % k)
    
    for tindex in range(len(pool_states)):

        type_specification = problem.type_specifications[pool_type_indices[tindex]]
    
        pool_states[tindex] = generator.leapfrog_distance_2_mask(
            state=pool_states[tindex],
            type_specification=type_specification,
            test_set=current_test_set,
            niteration=niteration,
            mask=pool_masks[tindex])
    
        print('%-2d : %3d' % (
            tindex,
            current_test_set.npass_state(state=pool_states[tindex]),
            ))
    
    pivot = np.argmax([current_test_set.npass_state(state=_) for _ in pool_states])
    
    print(pivot)
    
    constellation += [pool_states[pivot].copy()]
    constellation_type_indices += [pool_type_indices[pivot]]

    print('Constellation npass: %d' % (problem.test_set.npass_constellation(constellation=constellation)))

    indices = problem.test_set.passes_constellation(constellation=constellation)
    
    indices2 = [_ for _ in range(problem.test_set.ntest) if _ not in indices]

    current_test_set = bmw.TestSet(
        counts=[problem.test_set.counts[_] for _ in indices2],
        expressions=[problem.test_set.expressions[_] for _ in indices2],
        )

indices = problem.test_set.passes_constellation(constellation=constellation)

indices2 = [_ for _ in range(problem.test_set.ntest) if _ not in indices]

print('Failing Rules:')
for i2, index in enumerate(indices2):

    print('%1d : %s' % (
        problem.test_set.counts[index],
        problem.test_set.expressions[index]))

np.savez(
    'test.npz',
    constellation=constellation,
    constellation_type_indices=constellation_type_indices,
    )






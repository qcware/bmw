import bmw
import numpy as np

problem = bmw.Problem.parse(filepath='../../data/3-refined')

dat = np.load('test5.npz')

constellation = dat['constellation']
constellation_types = dat['constellation_types']

print(problem.test_set.npass_constellation(constellation))

generator = bmw.RandomStateGenerator.build_random_seed()

constellation = generator.improve_constellation(
    constellation=constellation,
    constellation_types=constellation_types,
    problem=problem,
    niteration=100000,
    )

print(problem.test_set.npass_constellation(constellation))

indices = problem.test_set.passes_constellation(constellation=constellation)

indices2 = [_ for _ in range(problem.test_set.ntest) if _ not in indices]

print('Failing Rules:')
for i2, index in enumerate(indices2):

    print('%1d : %s' % (
        problem.test_set.counts[index],
        problem.test_set.expressions[index]))

np.savez(
    'test6.npz',
    constellation=constellation,
    constellation_types=constellation_types,
    )

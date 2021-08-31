import bmw
import numpy as np

problem = bmw.Problem.parse(filepath='../../data/3-refined')

dat1 = np.load('test7.npz')
dat2 = np.load('test10.npz')

constellation1 = dat1['constellation']
constellation2 = dat2['constellation']

constellation = np.vstack((constellation1, constellation2))

constellation_types1 = dat1['constellation_types']
constellation_types2 = dat2['constellation_types']

constellation_types = np.concatenate((constellation_types1, constellation_types2))

print(problem.test_set.npass_constellation(constellation1))
print(problem.test_set.npass_constellation(constellation2))
print(problem.test_set.npass_constellation(constellation))


indices = problem.test_set.passes_constellation(constellation=constellation)

indices2 = [_ for _ in range(problem.test_set.ntest) if _ not in indices]

print('Failing Rules:')
for i2, index in enumerate(indices2):

    print('%1d : %s' % (
        problem.test_set.counts[index],
        problem.test_set.expressions[index]))


generator = bmw.RandomStateGenerator.build_random_seed()

constellation = generator.improve_constellation(
    constellation=constellation,
    constellation_types=constellation_types,
    problem=problem,
    niteration=10000,
    )

print(problem.test_set.npass_constellation(constellation))

indices = problem.test_set.passes_constellation(constellation=constellation)

indices2 = [_ for _ in range(problem.test_set.ntest) if _ not in indices]

print('Failing Rules:')
for i2, index in enumerate(indices2):

    print('%1d : %s' % (
        problem.test_set.counts[index],
        problem.test_set.expressions[index]))

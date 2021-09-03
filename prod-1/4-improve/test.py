import bmw
import numpy as np

problem = bmw.Problem.parse(filepath='../../data/3-refined')

dat = np.load('../2-prod/test-0.npz')
constellation = dat['constellation']
constellation_type_indices = dat['constellation_type_indices']

generator = bmw.RandomStateGenerator.build_random_seed()

for ncar in range(1, 60+1):

    constellation1 = constellation[:ncar, :]
    constellation_type_indices1 = constellation_type_indices[:ncar]

    constellation2 = generator.improve_constellation(
        constellation=constellation1,
        constellation_types=constellation_type_indices1,
        problem=problem,
        niteration=300000,
        )

    print('%-2d : %3d %3d' % (
        ncar,
        problem.test_set.npass_constellation(constellation1),
        problem.test_set.npass_constellation(constellation2),
        ))

    np.savez('constellation-%d.npz' % (ncar),
        constellation=constellation2,
        constellation_type_indices=constellation_type_indices1,
        )

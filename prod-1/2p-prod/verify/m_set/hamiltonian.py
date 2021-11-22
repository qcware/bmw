import bmw 
import numpy as np

def binary_indices(index):
    
    return [index2 for index2, char in enumerate(bin(index)[2:][::-1]) if char == '1']

if __name__ == '__main__':

    bmw_path = '/home/ec2-user/bmw'
    problem = bmw.Problem.parse(filepath='%s/data/3-refined' % bmw_path)

    M = 8
    dat = np.load('set_8.npz')
    constellation = dat['constellation']
    constellation_type_indices = dat['constellation_type_indices']

    test_set = problem.test_set

    print('%11s : %30s %30s %11s %11s' % (
        'Index(int)',
        'Index(bin)',
        'Index(inds)',
        'Popcount',
        'Score',
        ))

    hamiltonian = np.zeros((2**M,), dtype=np.float64)
    for index in range(2**M):
        indices = binary_indices(index=index)
        constellation2 = constellation[indices, :]
        constellation_type_indices2 = constellation_type_indices[indices]
        value = test_set.npass_constellation(constellation=constellation2)
        hamiltonian[index] = value
        print('%11d : %30s %30s %11d %11d' % (index, bin(index)[2:], indices, len(indices), value))

    np.savez(
        'hamiltonian-8.npz',
        hamiltonian=hamiltonian,
        )


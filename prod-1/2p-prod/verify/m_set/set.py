import numpy as np

np.set_printoptions(threshold=np.inf)

sol = np.load('../../test-6.npz')
constellation = sol['constellation']
constellation_type_indices = sol['constellation_type_indices']


constellation_m_6 = constellation[0:6,:]
constellation_type_indices_m_6 = constellation_type_indices[0:6]

constellation_m_8 = constellation[0:8,:]
constellation_type_indices_m_8 = constellation_type_indices[0:8]

constellation_m_16 = constellation[0:16,:]
constellation_type_indices_m_16 = constellation_type_indices[0:16]

np.savez(
    'set_6.npz',
    constellation=constellation_m_6,
    constellation_type_indices=constellation_type_indices_m_6,
    )

np.savez(
    'set_8.npz',
    constellation=constellation_m_8,
    constellation_type_indices=constellation_type_indices_m_8,
    )

np.savez(
    'set_16.npz',
    constellation=constellation_m_16,
    constellation_type_indices=constellation_type_indices_m_16,
    )


import numpy as np

np.set_printoptions(threshold=np.inf)

sol = np.load('../../test-6.npz')
constellation = sol['constellation']
constellation_type_indices = sol['constellation_type_indices']


constellation_m_12 = constellation[0:12,:]
constellation_type_indices_m_12 = constellation_type_indices[0:12]

constellation_m_14 = constellation[0:14,:]
constellation_type_indices_m_14 = constellation_type_indices[0:14]

constellation_m_24 = constellation[0:24,:]
constellation_type_indices_m_24 = constellation_type_indices[0:24]

np.savez(
    'set_12.npz',
    constellation=constellation_m_12,
    constellation_type_indices=constellation_type_indices_m_12,
    )

np.savez(
    'set_14.npz',
    constellation=constellation_m_14,
    constellation_type_indices=constellation_type_indices_m_14,
    )

np.savez(
    'set_24.npz',
    constellation=constellation_m_24,
    constellation_type_indices=constellation_type_indices_m_24,
    )


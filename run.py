import numpy as np
import lattice

lattice_test = lattice.lattice(3, 3, 3, 1, 1, 1, np.array([np.array([0, 0, 0])]), np.array([0.5, 0.5, 0]), np.array([0.5, 0, 0.5]), np.array([0, 0.5, 0.5]), "sc")

# sc bravais basis lattice vectors: np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])
# fcc bravais basis lattice vectors:  np.array([0.5, 0.5, 0]), np.array([0.5, 0, 0.5]), np.array([0, 0.5, 0.5])

#print(lattice_test.metric_lattice)
lattice_test.visualize(True)
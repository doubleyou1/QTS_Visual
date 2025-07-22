import numpy as np
import lattice
import lattice_dash
from dash import Dash, dcc, html, Output, Input
a_x = 1
a_z = 0.5


# sc bravais basis lattice vectors: a*(np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1]))
# fcc bravais basis lattice vectors:  a*(np.array([0.5, 0.5, 0]), np.array([0.5, 0, 0.5]), np.array([0, 0.5, 0.5]))
# bcc bravais basis lattice vectors: a*(np.array([-0.5, 0.5, 0.5]), np.array([0.5, -0.5, 0.5]), np.array([0.5, 0.5, -0.5]))
# hexagonal lattice: a_x*np.array([1, 0, 0]), np.array([0.5, a_x*np.sqrt(3)/2, 0]), a_z*np.array([0, 0, 1])
# graphite lattice 4 atomic basis: np.array([np.array([0, 0, 0]), np.array([1/3, 2/3, 0]), np.array([0, 0, 1/2]), np.array([2/3, 1/3, 1/2])))

#print(lattice_test.metric_lattice)
#lattice_test.visualize()


if __name__ == '__main__':
    lat = lattice.lattice([-2,2], [-2,2], [-2,2], 
                          a_x, a_x, a_z, 
                          np.array([np.array([0,0,0])]),
                          a_x/2*np.array([1, 0, 0]),  a_x/2*np.array([-1, np.sqrt(3)/2, 0]), a_z*np.array([0, 0, 1]), "sh")
    vis = lattice.LatticeVisualizer(lat)
    vis.run(debug=True)
    
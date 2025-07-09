import plotly.graph_objects as go
import numpy as np
from scipy.spatial import Voronoi, ConvexHull
import itertools

# Function to generate BCC lattice points
def generate_bcc_lattice(a=1.0, nx=2, ny=2, nz=2):
    # BCC primitive basis positions
    basis = np.array([
        [0, 0, 0],         # corner
        [0.5, 0.5, 0.5]    # body center
    ])

    lattice_points = []
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                origin = np.array([i, j, k])
                for b in basis:
                    point = a * (origin + b)
                    lattice_points.append(point)

    return np.array(lattice_points)

# Generate BCC lattice points
a = 1.0  # lattice constant
nx, ny, nz = 2, 2, 2  # number of unit cells in each direction
points = generate_bcc_lattice(a, nx, ny, nz)

# Create a 3D scatter plot
fig = go.Figure()

fig.add_trace(go.Scatter3d(
    x=points[:, 0],
    y=points[:, 1],
    z=points[:, 2],
    mode='markers',
    marker=dict(
        size=5,
        color='red',
        opacity=0.8
    )
))

def add_wigner_seitz_cell(fig, a=1.0, basis_coord=[0,0,0]):
    # Central atom + nearest neighbors in BCC
    basis = np.array([
    [0 + basis_coord[0], 0 + basis_coord[1], 0 + basis_coord[2]],  # center
    [0.5 + basis_coord[0], 0.5 + basis_coord[1], 0.5 + basis_coord[2]],
    [-0.5 + basis_coord[0], 0.5 + basis_coord[1], 0.5 + basis_coord[2]],
    [0.5 + basis_coord[0], -0.5 + basis_coord[1], 0.5 + basis_coord[2]],
    [0.5 + basis_coord[0], 0.5 + basis_coord[1], -0.5 + basis_coord[2]],
    [-0.5 + basis_coord[0], -0.5 + basis_coord[1], 0.5 + basis_coord[2]],
    [-0.5 + basis_coord[0], 0.5 + basis_coord[1], -0.5 + basis_coord[2]],
    [0.5 + basis_coord[0], -0.5 + basis_coord[1], -0.5 + basis_coord[2]],
    [-0.5 + basis_coord[0], -0.5 + basis_coord[1], -0.5 + basis_coord[2]]
    ]) * a  

    vor = Voronoi(basis)
    region_index = vor.point_region[0]
    region = vor.regions[region_index]

    if -1 in region or len(region) == 0:
        print("Unbounded or empty Voronoi region!")
        return

    vertices = vor.vertices[region]
    hull = ConvexHull(vertices)

    # Add Wigner-Seitz polyhedron as semi-transparent blue mesh
    fig.add_trace(go.Mesh3d(
        x=vertices[:, 0],
        y=vertices[:, 1],
        z=vertices[:, 2],
        i=hull.simplices[:, 0],
        j=hull.simplices[:, 1],
        k=hull.simplices[:, 2],
        opacity=0.4,
        color='deepskyblue',
        name='Wigner-Seitz Cell'
    ))

    # Optionally add black lines on the edges of the polyhedron for contrast
    edges = set()
    for triangle in hull.simplices:
        for i, j in itertools.combinations(triangle, 2):
            edge = tuple(sorted((i, j)))
            edges.add(edge)

    x_lines = []
    y_lines = []
    z_lines = []
    for i, j in edges:
        x_lines += [vertices[i][0], vertices[j][0], None]
        y_lines += [vertices[i][1], vertices[j][1], None]
        z_lines += [vertices[i][2], vertices[j][2], None]

    fig.add_trace(go.Scatter3d(
        x=x_lines, y=y_lines, z=z_lines,
        mode='lines',
        line=dict(color='black', width=3),
        name='WS Cell Edges',
        showlegend=False
    ))

# Add the Wigner-Seitz cell to the plot
add_wigner_seitz_cell(fig, a, [nx/2, ny/2, nz/2])


# Layout configuration
fig.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectmode='data'
    ),
    title='BCC Lattice',
    margin=dict(l=0, r=0, b=0, t=30)
)

# Save as HTML
fig.write_html("bcc_lattice.html")
print("BCC lattice visualization saved as bcc_lattice.html")

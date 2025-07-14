import plotly.graph_objects as go
import numpy as np
from scipy.spatial import Voronoi, ConvexHull
import itertools

# Function to generate BCC lattice points
def generate_bcc_lattice(a=1.0, nx=2, ny=2, nz=2, easy=True):

    if easy:
        lattice_points = [[0,0,0], [1,1,1], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [1,0,1], [0,1,1], [0.5, 0.5, 0.5],
                          [-0.5, 0.5, 0.5], [1.5, 0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 1.5, 0.5], [0.5, 0.5, -0.5], [0.5, 0.5, 1.5]]
    else:
        basis = np.array([
            [0, 0, 0],
            [0.5, 0.5, 0.5]
        ])

        lattice_points = []
        for i in range(-nx, nx + 1):
            for j in range(-ny, ny + 1):
                for k in range(-nz, nz + 1):
                    origin = np.array([i, j, k])
                    if i != nx and j != ny and k != nz:
                        for b in basis:
                            point = a * (origin + b)
                            lattice_points.append(point)

    return np.array(lattice_points)

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
    [-0.5 + basis_coord[0], -0.5 + basis_coord[1], -0.5 + basis_coord[2]],
    [1 + basis_coord[0], 0 + basis_coord[1], 0 + basis_coord[2]],
    [-1 + basis_coord[0], 0 + basis_coord[1], 0 + basis_coord[2]],
    [0 + basis_coord[0], 1 + basis_coord[1], 0 + basis_coord[2]],
    [0 + basis_coord[0], -1 + basis_coord[1], 0 + basis_coord[2]],
    [0 + basis_coord[0], 0 + basis_coord[1], 1 + basis_coord[2]],
    [0 + basis_coord[0], 0 + basis_coord[1], -1 + basis_coord[2]]
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
        opacity=0.25,  # lighter transparency
        color='lightblue',
        name='Wigner-Seitz Cell',
        showscale=False
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

def add_primitive_unit_cell(fig, a=1.0, origin=np.array([0, 0, 0]), color='green'):
    # BCC primitive vectors
    a1 = 0.5 * a * np.array([1, 1, -1])
    a2 = 0.5 * a * np.array([-1, 1, 1])
    a3 = 0.5 * a * np.array([1, -1, 1])

    # Define the 8 vertices of the parallelepiped
    vertices = np.array([
        origin,
        origin + a1,
        origin + a2,
        origin + a3,
        origin + a1 + a2,
        origin + a1 + a3,
        origin + a2 + a3,
        origin + a1 + a2 + a3
    ])

    # Define the edges to connect the vertices (12 edges of the parallelepiped)
    edge_indices = [
        (0, 1), (0, 2), (0, 3),
        (1, 4), (1, 5),
        (2, 4), (2, 6),
        (3, 5), (3, 6),
        (4, 7), (5, 7), (6, 7)
    ]

    x_lines, y_lines, z_lines = [], [], []
    for i, j in edge_indices:
        x_lines += [vertices[i][0], vertices[j][0], None]
        y_lines += [vertices[i][1], vertices[j][1], None]
        z_lines += [vertices[i][2], vertices[j][2], None]

    fig.add_trace(go.Scatter3d(
        x=x_lines, y=y_lines, z=z_lines,
        mode='lines',
        line=dict(color=color, width=4),
        name='Primitive Unit Cell'
    ))

# Generate BCC lattice points
a = 1.0  # lattice constant
nx, ny, nz = 1, 1, 1  # number of unit cells in each direction
points = generate_bcc_lattice(a, nx, ny, nz, True)

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

# stopp: nächste Mal korrigieren der WSC drawing
# wie besser Koordinaten System darstellen



# Layout configuration
fig.update_layout(
    scene=dict(
        xaxis=dict(
            title='X',
            showgrid=False,
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=2,
            showline=True,
            linecolor='black',
            mirror=True,
            showbackground=False,
        ),
        yaxis=dict(
            title='Y',
            showgrid=False,
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=2,
            showline=True,
            linecolor='black',
            mirror=True,
            showbackground=False,
        ),
        zaxis=dict(
            title='Z',
            showgrid=False,
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=2,
            showline=True,
            linecolor='black',
            mirror=True,
            showbackground=False,
        ),
        aspectmode='data'
    ),
    scene_camera=dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=1.5, y=1.5, z=1.2)
    ),
    title='BCC Lattice with Wigner-Seitz Cell',
    margin=dict(l=10, r=10, b=10, t=30),
    showlegend=True
)
# Layout configuration
# fig.update_layout(
#     scene=dict(
#         xaxis_title='X',
#         yaxis_title='Y',
#         zaxis_title='Z',
#         aspectmode='data'
#     ),
#     title='BCC Lattice',
#     margin=dict(l=0, r=0, b=0, t=30)
# )

# Add the Wigner-Seitz cell to the plot
add_wigner_seitz_cell(fig, a, [0.5, 0.5, 0.5])
#add_primitive_unit_cell(fig, a=1.0)

# Save as HTML
fig.write_html("bcc_lattice.html")
print("BCC lattice visualization saved as bcc_lattice.html")

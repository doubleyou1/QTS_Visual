import plotly.graph_objects as go
import numpy as np

# Function to generate FCC lattice points
def generate_fcc_lattice(a=1.0, nx=2, ny=2, nz=2):
    # FCC primitive basis positions
    basis = np.array([
        [0, 0, 0],
        [0.5, 0.5, 0],
        [0.5, 0, 0.5],
        [0, 0.5, 0.5]
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

# Generate FCC lattice points
a = 1.0  # lattice constant
nx, ny, nz = 3, 3, 3  # number of unit cells in each direction
points = generate_fcc_lattice(a, nx, ny, nz)

print(points)

# # Create a 3D scatter plot
# fig = go.Figure()

# fig.add_trace(go.Scatter3d(
#     x=points[:, 0],
#     y=points[:, 1],
#     z=points[:, 2],
#     mode='markers',
#     marker=dict(
#         size=5,
#         color='blue',
#         opacity=0.8
#     )
# ))

# # Layout configuration
# fig.update_layout(
#     scene=dict(
#         xaxis_title='X',
#         yaxis_title='Y',
#         zaxis_title='Z',
#         aspectmode='data'
#     ),
#     title='FCC Lattice',
#     margin=dict(l=0, r=0, b=0, t=30)
# )

# # Save as HTML
# fig.write_html("fcc_lattice.html")
# print("FCC lattice visualization saved as fcc_lattice.html")

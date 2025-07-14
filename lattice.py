import numpy as np
import plotly.graph_objects as go

class lattice:

    def __init__(self, length_x: float, length_y: float, length_z: float, a_x: float, a_y: float, a_z: float, atomic_basis: np.array, basis_vec_x: np.array, basis_vec_y: np.array, basis_vec_z: np.array,  structure_type: str):
        self.length_x = length_x
        self.length_y = length_y
        self.length_z = length_z
        self.a_x = a_x
        self.a_y = a_y
        self.a_z = a_z
        self.atomic_basis = atomic_basis
        self.structure_type = structure_type
        self.basis_vec_x = basis_vec_x
        self.basis_vec_y = basis_vec_y
        self.basis_vec_z = basis_vec_z

        # construct
        self.countable_lattice = np.zeros((int(self.length_x/self.a_x), int(self.length_y/self.a_y), int(self.length_z/self.a_z), len(self.atomic_basis)))
        self.metric_lattice = []
        self.nx = int(self.length_x/self.a_x)
        self.ny = int(self.length_y/self.a_y)
        self.nz = int(self.length_z/self.a_z)
        for i in range(self.nx):
            for j in range(self.ny):
                for k in range(self.nz):
                    for l in range(len(self.atomic_basis)):
                        self.countable_lattice[i][j][k][l] = 1
                        self.metric_lattice.append(i*self.basis_vec_x + j*self.basis_vec_y + k*self.basis_vec_z + l*self.atomic_basis[l]) 
        self.metric_lattice = np.array(self.metric_lattice)


    def visualize(self, basis_vector: bool): #, metric_lattice
        # Create a 3D scatter plot
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(
            x=self.metric_lattice[:, 0],
            y=self.metric_lattice[:, 1],
            z=self.metric_lattice[:, 2],
            mode='markers',
            marker=dict(
                size=5,
                color='blue',
                opacity=0.8
            )
        ))

    
        if basis_vector:
            # Add cones to show basis vectors
            self.basis_vectors = np.array([self.basis_vec_x, self.basis_vec_y, self.basis_vec_z])
            origin = np.array([0, 0, 0])

            colors = ['red', 'green', 'purple']
            labels = ['a1', 'a2', 'a3']
        

            # Add lines and cones for each basis vector
            for vec, color, label in zip(self.basis_vectors, colors, labels):
                # Line (shaft of arrow)
                fig.add_trace(go.Scatter3d(
                    x=[origin[0], vec[0]],
                    y=[origin[1], vec[1]],
                    z=[origin[2], vec[2]],
                    mode='lines+text',
                    line=dict(color=color, width=6),
                    text=[None, label],
                    textposition='top center',
                    showlegend=False
                ))

                # Cone (arrowhead)
                fig.add_trace(go.Cone(
                    x=[vec[0]],
                    y=[vec[1]],
                    z=[vec[2]],
                    u=[vec[0]],
                    v=[vec[1]],
                    w=[vec[2]],
                    sizemode='absolute',
                    sizeref=0.15,
                    anchor='tip',
                    colorscale=[[0, color], [1, color]],  # single-color scale
                    showscale=False,
                    opacity=1.0
                ))


        # Buttons for toggling visibility
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    direction="down",
                    x=1.1,
                    y=0.8,
                    showactive=True,
                    buttons=list([
                        dict(
                            label="Show All",
                            method="update",
                            args=[{"visible": [True] * len(fig.data)}]
                        ),
                        dict(
                            label="Hide Lattice Points",
                            method="update",
                            args=[{"visible": [False] + [True] * (len(fig.data) - 1)}]
                        ),
                        dict(
                            label="Hide Basis Vectors",
                            method="update",
                            args=[{"visible": [True] + [False] * (len(fig.data) - 1)}]
                        ),
                        dict(
                            label="Hide All",
                            method="update",
                            args=[{"visible": [False] * len(fig.data)}]
                        ),
                    ]),
                )
            ]
        )


        fig.update_layout(
            scene=dict(
                xaxis=dict(title='X', range=[-1, 2]),  # Fix x-axis range
                yaxis=dict(title='Y', range=[-1, 2]),  # Fix y-axis range
                zaxis=dict(title='Z', range=[-1, 2]),  # Fix z-axis range
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)  # Set fixed camera position
                ),
                aspectmode='data',
            ),
            title='FCC Lattice with Toggle Buttons',
            margin=dict(l=0, r=0, b=0, t=30)
        )

        # Save as HTML
        fig.write_html("lattice.html")
        print("lattice visualization saved as lattice.html")
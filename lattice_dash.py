import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Output, Input


class LatticeVisualizer:
    def __init__(self, range_x, range_y, range_z, a_x, a_y, a_z,
                 atomic_basis, basis_vec_x, basis_vec_y, basis_vec_z):

        self.range_x = range_x
        self.range_y = range_y
        self.range_z = range_z
        self.a_x = a_x
        self.a_y = a_y
        self.a_z = a_z
        self.atomic_basis = atomic_basis
        self.basis_vectors = np.array([basis_vec_x, basis_vec_y, basis_vec_z])

        self.metric_lattice = []
        for i in range(int(range_x[0] / a_x), int(range_x[1] / a_x) + 1):
            for j in range(int(range_y[0] / a_y), int(range_y[1] / a_y) + 1):
                for k in range(int(range_z[0] / a_z), int(range_z[1] / a_z) + 1):
                    for l in range(len(atomic_basis)):
                        point = (i * basis_vec_x +
                                 j * basis_vec_y +
                                 k * basis_vec_z +
                                 atomic_basis[l])
                        self.metric_lattice.append(point)

        self.metric_lattice = np.array(self.metric_lattice)

    def get_figure(self, show_lattice=True, show_basis=True, show_unit_cell=True):
        fig = go.Figure()

        if show_lattice:
            fig.add_trace(go.Scatter3d(
                x=self.metric_lattice[:, 0],
                y=self.metric_lattice[:, 1],
                z=self.metric_lattice[:, 2],
                mode='markers',
                marker=dict(size=5, color='blue', opacity=0.8),
                name='Lattice Points'
            ))

        origin = np.array([0, 0, 0])
        colors = ['red', 'green', 'purple']
        labels = ['a1', 'a2', 'a3']

        if show_basis:
            for vec, color, label in zip(self.basis_vectors, colors, labels):
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
                    colorscale=[[0, color], [1, color]],
                    showscale=False,
                    opacity=1.0
                ))

        if show_unit_cell:
            unit_cell_corners = np.array([
                [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
                [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]
            ])
            edges = [
                (0, 1), (0, 2), (0, 3),
                (1, 4), (1, 5),
                (2, 4), (2, 6),
                (3, 5), (3, 6),
                (4, 7), (5, 7), (6, 7)
            ]
            for start, end in edges:
                fig.add_trace(go.Scatter3d(
                    x=[unit_cell_corners[start][0], unit_cell_corners[end][0]],
                    y=[unit_cell_corners[start][1], unit_cell_corners[end][1]],
                    z=[unit_cell_corners[start][2], unit_cell_corners[end][2]],
                    mode='lines',
                    line=dict(color='black', width=3),
                    showlegend=False
                ))

        fig.update_layout(
            scene=dict(
                xaxis=dict(title='X', range=self.range_x),
                yaxis=dict(title='Y', range=self.range_y),
                zaxis=dict(title='Z', range=self.range_z),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
                aspectmode='data'
            ),
            margin=dict(l=0, r=0, b=0, t=30),
            title='Interactive FCC Lattice'
        )

        return fig

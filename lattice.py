import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Output, Input
import dash

class lattice:

    def __init__(self, range_x: np.array, range_y: np.array, range_z: np.array, a_x: float, a_y: float, a_z: float, atomic_basis: np.array, basis_vec_x: np.array, basis_vec_y: np.array, basis_vec_z: np.array,  structure_type: str):
        self.range_x = range_x
        self.range_y = range_y
        self.range_z = range_z
        self.a_x = a_x
        self.a_y = a_y
        self.a_z = a_z
        self.atomic_basis = atomic_basis
        self.structure_type = structure_type
        self.basis_vec_x = basis_vec_x
        self.basis_vec_y = basis_vec_y
        self.basis_vec_z = basis_vec_z
        self.basis_vectors = np.array([self.basis_vec_x, self.basis_vec_y, self.basis_vec_z])

        # construct
        #self.countable_lattice = np.zeros((int(self.length_x/self.a_x), int(self.length_y/self.a_y), int(self.length_z/self.a_z), len(self.atomic_basis)))
        self.metric_lattice = []
        self.lower_nx = int(self.range_x[0]/self.a_x)
        self.upper_nx = int(self.range_x[1]/self.a_x)
        self.lower_ny = int(self.range_y[0]/self.a_y)
        self.upper_ny = int(self.range_y[1]/self.a_y)
        self.lower_nz = int(self.range_z[0]/self.a_z)
        self.upper_nz = int(self.range_z[1]/self.a_z)
        for i in range(self.lower_nx, self.upper_nx+1):
            for j in range(self.lower_ny, self.upper_ny+1):
                for k in range(self.lower_nz, self.upper_nz+1):
                    for l in range(len(self.atomic_basis)):
                        #self.countable_lattice[i][j][k][l] = 1
                        self.metric_lattice.append(i*self.basis_vec_x + j*self.basis_vec_y + k*self.basis_vec_z + l*self.atomic_basis[l]) 
        self.metric_lattice = np.array(self.metric_lattice)

    def get_figure(self, show_lattice=True, show_basis=True, show_unit_cell=True,
                camera=None, x_range=None, y_range=None, z_range=None):
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
                xaxis=dict(title='X', range=x_range or self.range_x),
                yaxis=dict(title='Y', range=y_range or self.range_y),
                zaxis=dict(title='Z', range=z_range or self.range_z),
                camera=camera or dict(eye=dict(x=1.5, y=1.5, z=1.5)),
                aspectmode='data',
            ),
            margin=dict(l=0, r=0, b=0, t=30),
            title="FCC Lattice"
        )

        return fig


class LatticeVisualizer:
    def __init__(self, lattice):
        self.lattice = lattice
        self.app = Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        self.app.layout = html.Div([
            html.H2("FCC Lattice Visualization"),
            dcc.Checklist(
                options=[
                    {'label': 'Lattice Points', 'value': 'lattice'},
                    {'label': 'Basis Vectors', 'value': 'basis'},
                    {'label': 'Unit Cell', 'value': 'unit_cell'}
                ],
                value=['lattice', 'basis', 'unit_cell'],
                id='toggle-options',
                labelStyle={'display': 'inline-block', 'margin': '10px'}
            ),
            dcc.Graph(id='lattice-graph', style={'height': '80vh'}),
            dcc.Store(id='camera-store'),  # store camera/zoom
        ])

    def setup_callbacks(self):
        @self.app.callback(
            Output('camera-store', 'data'),
            Input('lattice-graph', 'relayoutData'),
            prevent_initial_call=True
        )
        def save_camera_data(relayout_data):
            if not relayout_data:
                return dash.no_update

            return {
                'camera': relayout_data.get('scene.camera'),
                'x_range': relayout_data.get('scene.xaxis.range'),
                'y_range': relayout_data.get('scene.yaxis.range'),
                'z_range': relayout_data.get('scene.zaxis.range')
            }

        @self.app.callback(
            Output('lattice-graph', 'figure'),
            Input('toggle-options', 'value'),
            Input('camera-store', 'data')
        )
        def update_figure(selected, camera_data):
            camera = camera_data.get('camera') if camera_data else None
            x_range = camera_data.get('x_range') if camera_data else None
            y_range = camera_data.get('y_range') if camera_data else None
            z_range = camera_data.get('z_range') if camera_data else None

            return self.lattice.get_figure(
                show_lattice='lattice' in selected,
                show_basis='basis' in selected,
                show_unit_cell='unit_cell' in selected,
                camera=camera,
                x_range=x_range,
                y_range=y_range,
                z_range=z_range
            )

    def run(self, **kwargs):
        self.app.run(**kwargs)
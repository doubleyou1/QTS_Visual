import numpy as np
from scipy.special import genlaguerre
import plotly.graph_objs as go
from plotly.offline import plot
import math

# Beam parameters
z_r = 1
p = 0
l = 1
w_0 = 1
k = 2 * np.pi
omega = 2 * np.pi

# Grid in cylindrical coordinates
rho = np.linspace(0, np.pi, 100)
phi = np.linspace(0, 2 * np.pi, 100)
z_vals = np.linspace(0, 2, 50)
RHO, PHI, Z = np.meshgrid(rho, phi, z_vals, indexing='ij')
X = RHO * np.cos(PHI)
Y = RHO * np.sin(PHI)
z_idx = 25
z_fixed = z_vals[z_idx]

# Coordinate slices
X_slice = X[:, :, z_idx]
Y_slice = Y[:, :, z_idx]
RHO_slice = RHO[:, :, z_idx]
PHI_slice = PHI[:, :, z_idx]

# Functions
def wavefront_radius(z, z_r):
    return (z_r**2 + z**2) / z

def spot_radius(z, z_r, w_0):
    return w_0 * np.sqrt(1 + z**2 / z_r**2)

def guoy_phase(z, z_r, p, l):
    return (2*p + np.abs(l) + 1) * np.arctan(z / z_r)

def amplitude(rho, phi, z, z_r, p, l, w_0, k):
    temp1 = np.sqrt(2 * math.factorial(p) / (np.pi * math.factorial(p + np.abs(l))))
    temp2 = (np.sqrt(2) * rho / spot_radius(z, z_r, w_0))**np.abs(l)
    L = genlaguerre(p, np.abs(l))
    temp3 = L(2 * rho**2 / spot_radius(z, z_r, w_0)**2) * w_0 / spot_radius(z, z_r, w_0)
    temp4 = np.exp(-rho**2 / spot_radius(z, z_r, w_0)**2 
                   - 1j * k * rho**2 / (2 * wavefront_radius(z, z_r))
                   + 1j * l * phi 
                   - 1j * guoy_phase(z, z_r, p, l))
    return temp1 * temp2 * temp3 * temp4

def complex_amplitude(rho, phi, z, z_r, p, l, w_0, k, omega, t):
    amp = amplitude(rho, phi, z, z_r, p, l, w_0, k)
    return amp * np.exp(1j * (k * z - omega * t))

# Create frames for animation
frames = []
num_frames = 60

for i in range(num_frames):
    t = i / 15  # Time step
    Znew = np.real(complex_amplitude(RHO_slice, PHI_slice, z_fixed, z_r, p, l, w_0, k, omega, t))
    Znew /= np.max(np.abs(Znew))

    frame = go.Frame(
        data=[go.Surface(z=Znew, x=X_slice, y=Y_slice, colorscale='RdBu', cmin=-1, cmax=1)],
        name=str(i)
    )
    frames.append(frame)

# Initial data
Z0 = np.real(complex_amplitude(RHO_slice, PHI_slice, z_fixed, z_r, p, l, w_0, k, omega, 0))
Z0 /= np.max(np.abs(Z0))

# Plotly surface
surface = go.Surface(z=Z0, x=X_slice, y=Y_slice, colorscale='RdBu', cmin=-1, cmax=1)

layout = go.Layout(
    title='Interactive 3D Wave (Real Part)',
    scene=dict(
        zaxis=dict(range=[-1, 1]),
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Amplitude'
    ),
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        buttons=[dict(label='Play', method='animate', args=[None, {"frame": {"duration": 50}, "fromcurrent": True}])]
    )]
)

fig = go.Figure(data=[surface], layout=layout, frames=frames)

# Save to interactive HTML
plot(fig, filename='interactive_wave.html', auto_open=False)

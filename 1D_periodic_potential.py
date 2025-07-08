import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import constants as sc
from matplotlib.widgets import Slider

# # Constants and settings
num_atoms = 5
atom_spacing = 0.5
wave_amplitude = 0.5
wave_number = 2 * np.pi / atom_spacing
atom_radius = 0.1

# # Atom positions along x-axis
atom_positions_2d = np.array([[i * atom_spacing] for i in range(num_atoms)])


# # Plot wavefunction (electron density)
x_wave = np.linspace(-1*(int(num_atoms/2) - 1) * atom_spacing, (int(num_atoms/2) - 1) * atom_spacing, 500)
m = sc.m_e
hbar = sc.hbar
q =  2.283 / atom_spacing # [2.283, 3.141], [4.760, 6.281], [7.463, 9.424]
C = 1/ np.sqrt(2)
D = 1/ np.sqrt(2)
mag_psi = C**2*np.cos(q*x_wave)**2 + D**2*np.sin(q*x_wave)**2 + C*D*np.sin(2*q*x_wave) # könnte auch falsch sein 

# plt.scatter(atom_positions_2d, np.zeros(len(atom_positions_2d)))
# plt.plot(x_wave, mag_psi)
# plt.show()

# Example range for q
A = 7.463 #4.760 #2.283
B = 9.424# 6.281 #3.141

# Initial q
q0 = (A + B) / 2

# Create figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

# Initial plot
line, = ax.plot(x_wave, mag_psi)

ax.scatter(atom_positions_2d, np.zeros(len(atom_positions_2d)))
ax.set_title("Adjust q with the slider")
ax.legend()
ax.grid(True)

# Slider axis: [left, bottom, width, height]
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
slider_q = Slider(ax_slider, 'q', A, B, valinit=q0)

# Update function
def update(val):
    q = slider_q.val
    line.set_ydata(C**2*np.cos(q*x_wave)**2 + D**2*np.sin(q*x_wave)**2 + C*D*np.sin(2*q*x_wave))
    fig.canvas.draw_idle()

# Connect slider to update function
slider_q.on_changed(update)
ax.set_xlim(-1*(int(num_atoms/2) - 1) * atom_spacing, (int(num_atoms/2) - 1) * atom_spacing)

plt.show()

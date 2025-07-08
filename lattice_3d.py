import matplotlib.pyplot as plt
import numpy as np



fig = plt.figure()
ax = fig.add_subplot(projection='3d')

for i in range(5):
    for j in range(5):
        for k in range(5):
            ax.scatter(i,j,k, color = "tab:blue")


# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')
ax.set_axis_off()

plt.show()

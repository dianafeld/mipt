import matplotlib.pyplot as plt

#plt.plot([1,2,3,4])
#plt.ylabel('some numbers')
#plt.show()

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#Axes3D.plot_surface(X, Y, Z, *args, **kwargs)

X = np.arange(-10, 10, 0.25)
Y = np.arange(-5, 2000, 1)
X, Y = np.meshgrid(X, Y)
Z = (1 - X) ** 2 + 100 * (Y - X ** 2) ** 2

surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=0, antialiased=False)
ax.set_zlim(-1.01, 1.01)

plt.show()
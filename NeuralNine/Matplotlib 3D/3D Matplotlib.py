import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

#Single Points

ax = plt.axes(projection = "3d")
ax.scatter(3, 5, 7)
plt.show()


#Scatter Plots
ax = plt.axes(projection = "3d")
x_data = np.random.randint(0, 100, (500,))
y_data = np.random.randint(0, 100, (500,))
z_data = np.random.randint(0, 100, (500,))

ax.scatter(x_data, y_data, z_data, marker="+", alpha=0.5)
plt.show()


#Fonction plot
ax = plt.axes(projection = "3d")
x_data = np.arange(0, 50, 0.1)
y_data = np.arange(0, 50, 0.1)
z_data = x_data * y_data

ax.plot(x_data, y_data, z_data)
plt.show()

#Surface Plot
ax = plt.axes(projection = "3d")
x_data = np.arange(0, 50, 0.1)
y_data = np.arange(0, 50, 0.1)

X, Y = np.meshgrid(x_data, y_data)
Z = X * Y

ax.plot_surface(X, Y, Z)
plt.show()

#Surface Plot 2
ax = plt.axes(projection = "3d")
x_data = np.arange(-5, 5, 0.1)
y_data = np.arange(-5, 5, 0.1)

X, Y = np.meshgrid(x_data, y_data)
Z = np.sin(X) * np.cos(Y)

ax.plot_surface(X, Y, Z, cmap="plasma")
plt.show()



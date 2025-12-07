import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Y = [5, 7, 9, 2, 4, 1, 1, 9, 2, 3]
Z = [9, 7, 5, 8, 6, 4, 3, 2, 1, 0]

ax.scatter(X, Y, Z, c='r', marker='o')
ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')
plt.show()